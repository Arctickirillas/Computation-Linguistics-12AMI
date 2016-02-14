from lxml import etree
import locale
import sys
import codecs
import string
import re
import math
import cmath

############################################################
sys.stdout = codecs.getwriter('CP1251')(sys.stdout)
loc=locale.getlocale()
locale.setlocale(locale.LC_ALL, '')
############################################################

#словарик
mapping = dict()

#обработка твитов
def UpgradeStr(row):
    row = row.lower()
    row = row.strip()
    regex = re.compile('[%s]' % re.escape(string.punctuation + string.digits + string.ascii_letters))
    row = regex.sub('', row)
    row = row.split()  
    return row  

#обработка запроса из консоли, получаем вектор слов
def PreparePhrase():
    phrase = raw_input(u"Please enter the phrase").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    phrase = UpgradeStr(phrase)
    return phrase

#преобразование оценок в -1,0,1
def ClassifyMark(str):
        if (str == "-1"):
            return -1
        elif (str == "1"):
            return 1
        else:
            return 0

#общая оценка твита, если отлично от нуля, то обрабатываем этот твит, на выходе: общая оценка по 8-ми банкам
def EstimateTwit(element):
    est = 0
    for i in xrange(5,13):
       est  = est + ClassifyMark(element[i].text)

    if (est > 0):
        return 1
    elif (est < 0):
        return -1
    else:
        return 0

def calculateAiBi(element, relev):
    row = UpgradeStr(element[4].text)
    length = len(row)
        
    for word in row:
        if (mapping.get(word) == None):
            coef = [0.0, 0.0, 0.0] #ai, bi, ci
            if (relev == 1):
                coef[0] = coef[0] + 1.0/length
            else:
                coef[1] = coef[1] + 1.0/length
            mapping[word] = coef
        else:
            coef = mapping.get(word)
            if (relev == 1):
                coef[0] = coef[0] + 1.0/length
            else:
                coef[1] = coef[1] + 1.0/length
            mapping[word] = coef

def calculate_ci(count): 
    for word in mapping:
        coef = mapping.get(word)
        if (coef[1] == 0 or coef[0] == 1 or coef[0] == 0 or coef[1] == 1): 
            coef[2] = 0.0000001 
        else:
            coef[0] = coef[0]/float(count) #приводит к интервалу от 0 до 1
            coef[1] = coef[1]/float(count) #приводит к интервалу от 0 до 1
            coef[2] = math.log((coef[0]*(1 - coef[1]))/(coef[1]*(1 - coef[0])))
            mapping[word] = coef


def calculateC(): 
    C = 0.0
    for word in mapping:
        coef = mapping[word]
        if (coef[1] != 0 and coef[0] != 1 and coef[0] != 0 and coef[1] != 1): 
            C = C + math.log((1 - coef[0])/float(1 - coef[1])) 
        else:
            continue
    return C

def calculateGd():
    phrase = PreparePhrase()
    g = calculateC()
    for word in phrase:
        if word in mapping:
            g = g + mapping[word][2]
            print u" word: " + str(mapping[word][2])
        else:
            print u"No such word!"
    print u" C = " + str(calculateC())
    print u" g = " + str(g)


#запись в файл csv
def WriteInCSV():
    with open('names.csv', 'w') as csvfile:
        for word in mapping:
             csvfile.write (word.encode('CP1251') +';' + str(mapping[word][2]) + '\n')
        csvfile.write(u'C' +';' + str(calculateC()))



def CreateDictionary():
    count = 0
    #цикл по файлам
    for i in xrange(1, 51):
        tree = etree.parse('banks_train/bank ({fileIndex}).xml'.format(fileIndex = str(i)))
        root = tree.getroot()

        #цикл по твитам
        for element in root.iter ('table'):
            if (EstimateTwit(element) != 0):
                count = count + 1
                relev = EstimateTwit(element)
                calculateAiBi(element, relev)
    calculate_ci(count)
    calculateGd()


#########   main   ###############
CreateDictionary()
WriteInCSV()


############################################################
locale.setlocale(locale.LC_ALL, loc)