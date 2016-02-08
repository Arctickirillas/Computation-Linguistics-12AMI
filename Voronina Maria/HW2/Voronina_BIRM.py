from lxml import etree
from zipfile import *
import re
import string
import math

z = ZipFile('banks_train.zip', 'r')
z.extractall()
names = z.namelist()
print(names)
dictionary_relevant = dict({})
dictionary = dict({})
delete = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters + string.digits))
index = 0
for name in names:
    tree = etree.parse(name)
    root = tree.getroot()
    for element in root.iter('table'):
         for j in range(1, 9):
            if(element[4 + j].text == '1'):
                text = (delete.sub(' ', str(element[4].text))).split()
                for word in text:
                    if(dictionary_relevant.get(word) is None):
                        dictionary_relevant[word] = set()
                    dictionary_relevant[word].add(int(element[0].text))
                    if(dictionary.get(word) is None):
                        dictionary[word] = set()
                    dictionary[word].add(int(element[0].text))
            else:
                if(element[4 + j].text == '-1'):
                    text = delete.sub(' ', str(element[4].text)).split()
                    for word in text:
                        if dictionary.get(word) is None:
                            dictionary[word] = set()
                        dictionary[word].add(int(element[0].text))
         index = index + 1

ci = dict({})
r = len(dictionary_relevant)
n = len(dictionary)
c = 0
for word in dictionary:
    if dictionary_relevant.get(word) is not None:
        ri = len(dictionary_relevant[word])
        ai = ri/r
        ni = len(dictionary[word])
        bi = (ni - ri)/(n-r)
        ci[word] = math.log2(((ri+0.5)/(r-ri+0.5))/((ni-ri+0.5)/(n-ni-r+ri+0.5)))
        c += (math.log2((1-ai)/(1-bi)))

print (c)
file = open('answer.csv', 'w')
file.write('word')
file.write(';')
file.write('сi')
file.write('\n')
for word in ci:
    file.write(word+';')
    file.write(str(ci[word]))
    file.write('\n')
file.write('с = ')
file.write(str(c))
file.write(';')
file.write('\n')
file.close()

#line = 'Сбербанк дал деньги детям'
line = 'Москва хочет сотрудничать'
line = re.split('\.| |,|;', line)

g = c + sum(ci[word] for word in line)
print(g)

if g > c:
    print ('relevant')
else:
    print ('not relevant')

z.close()