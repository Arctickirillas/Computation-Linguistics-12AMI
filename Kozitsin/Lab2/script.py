# -*- coding: utf-8 -*-

from lxml import etree
import locale
import sys
import codecs
import math
import re
import string
 
# set locale for russian
sys.stdout = codecs.getwriter('CP1251')(sys.stdout)
loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, '')

# dictionary to store words
wordsMapping = dict()

def mark2Int(str):
    if (str == "1"):
        return 1
    elif (str == "-1"):
        return -1
    else:
        return 0

def validate(element):
    total = 0
    for i in xrange(5, 13):
        total = total + mark2Int(element[i].text)
    
    # relevant twit
    if (total > 0):
        return 1
    # irrelevant twit
    elif (total < 0):
        return -1
    # mess
    else:
        return 0

def removeSymbols(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters + string.digits))
    text = regex.sub(' ', text)
    words = text.split()
    return words

def processTwit(twit, processFlag):
    twitWords = removeSymbols(twit[4].text.lower())
    length = len(twitWords)

    for word in twitWords:
        if (word in wordsMapping):
            temp = wordsMapping.get(word)
            if (processFlag == 1):
                temp[0] = temp[0] + (1.0 / length) # update a_i
            else:
                temp[1] = temp[1] + (1.0 / length) # update b_i
            wordsMapping[word] = temp
        else:
            temp = [0.0, 0.0, 0.0]
            if (processFlag == 1):
                temp[0] = temp[0] + (1.0 / length) # update a_i
            else:
                temp[1] = temp[1] + (1.0 / length) # update b_i
            wordsMapping[word] = temp

def postProcess(twitCounter):
    keysForProcess = list()

    max = -10000  # small int
    min = 10000 # big int

    for word in wordsMapping:
        temp = wordsMapping.get(word)

        if (temp[0] == 0 or temp[0] == 1 or
            temp[1] == 0 or temp[1] == 1):
            keysForProcess.append(word)
            continue
        else:
            temp[0] = temp[0] / float(twitCounter)
            temp[1] = temp[1] / float(twitCounter)
            temp[2] = math.log( (temp[0] * (1 - temp[1])) / (temp[1] * (1 - temp[0])), math.e)

            if (temp[2] > max):
                max = temp[2]
            elif (temp[2] < min):
                min = temp[2]

            wordsMapping[word] = temp

    # postprocess
    for item in keysForProcess:
        temp = wordsMapping.get(item)
        temp[0] = temp[0] / float(twitCounter)
        temp[1] = temp[1] / float(twitCounter)

        if (temp[0] == 0 or temp[1] == 1): # this word determines irrelevant document,
            wordsMapping[item][2] = min    # so assign min weight
        elif (temp[1] == 0 or temp[1] == 1): # this word determines relevant document,
            wordsMapping[item][2] = max      # so assign max weight

def calcC():
    C = 0.0
    for word in wordsMapping:
        temp = wordsMapping[word]
        C = C + math.log( (1 - temp[0]) / float(1 - temp[1]), math.e)
    return C

def saveInCSV():
    with open('model.csv', 'a') as csvfile:
        for word in wordsMapping:
            csvfile.write(word.encode('CP1251') + ';' + str(wordsMapping[word][2]) + '\n')

        csvfile.write(u'C;' + str(calcC()))

def calcG(input):
    input = removeSymbols(input.lower())
    g = calcC()
    for word in input:
        if word in wordsMapping:
            g =  g + wordsMapping[word][2]
    print u"g(d) = " + str(g)

##############################################
#              main body                     #
##############################################
FILE_NUM = 51
processFlag = 0 # 1, 0, -1

twitCounter = 0

# main loop
for i in xrange(1, FILE_NUM):
    tree = etree.parse('banks_train/bank ({fileIndex}).xml'.format(fileIndex = str(i)))
    root = tree.getroot()

    # inside loop on twits in one file
    for element in root.iter ('table'):
        processFlag = validate(element)
        if (processFlag != 0):
            twitCounter = twitCounter + 1
            processTwit(element, processFlag)
        else:
            continue

postProcess(twitCounter)
saveInCSV()

input = raw_input(u"Введите фразу: ").decode(sys.stdin.encoding or locale.getpreferredencoding(True))
calcG(input)

# return original locale
locale.setlocale(locale.LC_ALL, loc)