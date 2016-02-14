import xml.etree as etree
import xml.etree.ElementTree as et
import re
import string
import math

regex = re.compile('[%s]' % re.escape(string.punctuation))
dictionaryRelevant = dict()
dictionary = dict()
index = 0
def makeIndex(dictionary,str,index):
    words=str
    for word in words:
        if (dictionary.get(word.lower()) == None):
            dictionary[word.lower()] = set()
        dictionary[word.lower()].add(index)
    #index += 1
    return dictionary

for i in range(1, 51):
    bank = 'banks/bank (' + str(i) + ').xml'
    tree = et.parse(bank)
    root = tree.getroot()
    for child in root.iter('table'):
        for j in range(1, 9):
            if(child[4 + j].text == '1'):
                text = (str(regex.sub(' ', str(child[4].text)))).split()
                makeIndex(dictionaryRelevant,text,child[0].text)
                makeIndex(dictionary,text,child[0].text)
                break
            else:
                if(child[4 + j].text == '-1'):
                    text = regex.sub(' ', str(child[4].text)).split()
                    makeIndex(dictionary,text,child[0].text)
                    break
        index += 1


ci = dict({})
r = len(dictionaryRelevant)
n = len(dictionary)
c = 0
for word in dictionary:
    if dictionaryRelevant.get(word) is not None:
        ri = len(dictionaryRelevant[word])
        ai = ri/r
        ni = len(dictionary[word])
        bi = (ni - ri)/(n-r)
        ci[word] = math.log(((ri+0.5)/(r-ri+0.5))/((ni-ri+0.5)/(n-ni-r+ri+0.5)))
        c += (math.log((1-ai)/(1-bi)))

print(ci)
f = open('result.csv', 'w')
for word in ci:
    f.write(word+';')
    f.write(str(ci[word]))
    f.write('\n')
f.write('\nC;'+str(c)+'\n')
f.close()

input = 'Сбербанк кредит'
input=input.split()

result = c
for word in input:
    if ci.get(word) is not None:
        result += ci[word]
print(result)