__author__ = 'Mironov Alexander'

import re
import csv
from scipy.sparse import csr_matrix
import numpy as np
#split words 


titleArray = []
textArray = []
wordI = []
pre_index = []#word in wordI
index = []
with open("/Users/mironoff/Desktop/4.csv",'rt') as csvfile:
            table = csv.reader(csvfile, delimiter=';' )
            for t,row in enumerate(table):
                pre_index = [0]*len(pre_index)
                #print (row)#row every string
                titleArray.append(row[0])
                words = (re.split("[\s;:\-_*\".,?!()]", row[1]))#split row
                for word in words:
                    #print (word)
                    if word != '' and word not in wordI:
                        wordI.append(word)
                        pre_index.append(1)
                    elif word in wordI:
                        pre_index[wordI.index(word)] += 1
                #print(wordI,pre_index)
                index.append(pre_index)  
for i in range(10):       
    for j in range(len(wordI)-len(index[i])):
        index[i].append(0)          
index = (csr_matrix(index))
print(index)
print (wordI[10])

# query

phrase = input()
phrase = (re.split("[\s;:\-_*\".,?!()]", phrase))

# phrase = ['doing']
try:
    table = np.zeros((10,len(phrase)))
    for w,word in enumerate(phrase):
        for i in range(10):
            try:
                element=index.getrow(i).getcol(wordI.index(word))
                if element>0:#have in text word
                    table[i][w] = element.toarray()[0][0]
            except Exception:
                    print('Word '+word+' not found!')
                    break
    print(table)
except Exception:
    print('Phrase not found')
