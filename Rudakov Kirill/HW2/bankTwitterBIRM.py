__author__ = 'Kirill Rudakov'

from os import listdir
import xml.etree.ElementTree as ET
import re
import numpy as np
import pandas as pd
import pymorphy2

# deleted http//..., numbers and simbols (including #), RT and users, all English char
symbolsInspector = re.compile(r'([–…=·~—#”“\*$€№.«»?\-!&,+%\"\|:;()\/\']|http[.:/a-zA-Z0-9]*|[@a-zA-z0-9]|RT)')

# stopwords
stopword = []
file = open('stopword.txt','r')
for row in file:
    stopword.append(row[:-1])
file.close()
# print(stopword)

dictionary = set([])
positiveIndex = []
negativeIndex = []

# word to the normal form
morph = pymorphy2.MorphAnalyzer()

# POSITIVE - 356, NEGATIVE - 1066, NEUTRAL - other are not considered
fileList = listdir("BankTrain")
for pathToXML in fileList:
    tree = ET.parse('BankTrain/'+pathToXML)
    root = tree.getroot()
    for j,element in enumerate(root.iter('table')):
        def obtainInvertedIndex(dictionary):
            field = dict(zip(dictionary,np.zeros(len(dictionary))))
            for word in splittedLine:
                if word in field:
                    field[word] += 1.
            return field

        splittedLine =(symbolsInspector.sub('',element[4].text).lower().split())
        clearLine = []
        for word in splittedLine:
            if word not in stopword:
                p = morph.parse(word)[0]
                clearLine.append(p.normal_form)


        dictionary = dictionary.union(set(clearLine))

        for i in range(0,8,1):
             if element[i+5].text == '1':
                positiveIndex.append(obtainInvertedIndex(dictionary))
                break
             elif element[i+5].text == '-1':
                negativeIndex.append(obtainInvertedIndex(dictionary))
                break

# TWO Frame
dataFramePos = pd.DataFrame(positiveIndex).fillna(0)
dataFrameNeg = pd.DataFrame(negativeIndex).fillna(0)

# -- BIRM Functions
def getR_i(query):
    toReturn = []
    for word in query:
        if word in dataFramePos:
            r = sum(dataFramePos[word])
            toReturn.append(r)
        else:
            toReturn.append(0.)
    return toReturn

def getR():
    return len(positiveIndex)
def getN():
    return len(positiveIndex+negativeIndex)
def getN_i(query):
    toReturn = []
    for word in query:
        if word in dataFramePos or word in dataFrameNeg:
            n = sum(dataFramePos[word]) + sum(dataFrameNeg[word])
            toReturn.append(n)
        else:
            toReturn.append(0.)
    return toReturn
def getC_i(N,R,listOfR,listOfN):
    listOfC = []
    C = 0
    for i in range(len(listOfR)):
        a = listOfR[i]/R
        b = (listOfN[i] - listOfR[i])/(N - R)
        C += np.log((1-a)/(1-b))
        # to keep c_i value from being infinite added + 0.5
        #     c_i = np.log((a*(1-b))/(b*(1-a)))
        c_i = np.log((listOfR[i]+0.5)*(N-listOfN[i]-R+listOfR[i]+0.5)/((R-listOfR[i]+0.5)*(listOfN[i]-listOfR[i]+0.5)))

        listOfC.append(c_i)
    return listOfC,C
def getG(listOfC,C):
    return sum(listOfC),sum(listOfC)+C

# -- MAIN
print('Введите запрос:')
preQuery = input()
preQuery = symbolsInspector.sub('',preQuery).lower().split()
query = []
for word in preQuery:
    p = morph.parse(word)[0]
    query.append(p.normal_form)

# obtaining all main vars
listOfN,listOfR,R,N = (getN_i(query),getR_i(query),getR(),getN())

listOfC,C = getC_i(N,R,listOfR,listOfN)

g,gFull = getG(listOfC,C)

if g > 0:
    print('Принадлежность к классу: +1.')
elif g < 0:
    print('Принадлежность к классу: -1.')
elif g == 0:
    print('О приндалежности к одному из классов сказать ничего нельзя!')
print('Дополнительно: \ng - C = '+str(g)+'; где C = '+str(C))

# Write to csvFile
file = open('coefficients.csv', 'w')
header = 'word_i;c_i;C\n'
file.write(header)
for i,word in enumerate(query):
    file.write(str(word)+';'+str(listOfC[i])+'\n')
file.write(';;'+str(C))
file.close()