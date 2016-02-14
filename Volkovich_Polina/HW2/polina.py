from lxml import etree
from zipfile import *
import re
import string
import math

names = []
lala = []
lines = {}
is_zipfile('bank_train.zip')
z = ZipFile('banks_train.zip', 'r')
z.extractall()
names = z.namelist()
#print(names)
wella = []
releva = []
i=0
j=0
diction = dict()
for name in names:
    tree = etree.parse(name)
    root = tree.getroot()
    for element in root.iter('table'):
        wella = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters + string.digits))
        lala = wella.sub(' ', str(element[4].text))
        text = lala.split()
        #print (text)
        for word in text:
            if diction.get(word) == None:
                    diction[word] = []
            diction[word].append(i)
        i = i + 1
        for j in range(5,13):
            if (element[j].text == '1'):
                releva.append(1)
                break
            else:
                if (element[j].text == '-1'):
                    releva.append(-1)
                    break
                else:
                    releva.append(0)
                    break
#print (len(releva))
#print (releva)
#print (diction)
R=0
for s in range(0, len(releva)):
    if releva[s] == 1:
        R = R+1
#print (R)
N=0
for a in range(0, len(releva)):
    if releva[a] == 1 or releva[a] == -1:
        N = N +1
#print(N)
ci = dict({})
C=0
for w in diction:
    ri=0
    ni=0
    for num in diction[w]:
        if releva[num-1] == 1:
            ri=ri+1
            ni=ni+1
        else:
            if releva[num-1] == -1:
                ni=ni+1
    ai = ri/R
    bi = (ni - ri)/(N-R)
    ci[w] = math.log2(((ri+0.5)/(R-ri+0.5))/((ni-ri+0.5)/(N-ni-R+ri+0.5)))
    C = C + (math.log2((1-ai)/(1-bi)))
#print(C)
f = open('volkovich.csv', 'w')
for word in ci:
    f.write(word+';')
    f.write(str(ci[word]))
    f.write('\n')
f.write('C;'+ str(C))
f.close()

new_word = 'Ряд российских олигархов'
new_word = re.split('\.| |,|;', new_word)

result = C
for word in new_word:
    if ci.get(word) is not None:
        result = result + ci[word]
    else:
        print('Ошибка!')
print('Результа запроса:', result)

