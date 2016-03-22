#!/usr/bin/env python

import math

input_file = open('3grams-3.txt', mode='r', encoding='utf-8')

grams = {}
no_line = 0
for i in input_file:
    i = i[0:-1]
    words = i.split(sep = '\t')
    gram=''
    gram = words[1] + ' ' + words[3] + ' ' + words[5]
    #print(gramma)
    grams[gram] = float(words[0])/35973

input_file.close()



querygrams={}
for sentence in open("sentences.txt"):
        i = i[0:-1]
        words = sentence.split()
        for k in range(0, len(words)-2):
            str = words[k] + ' ' + words[k+1] + ' ' + words[k+2]
            for gram in grams:
                if (grams.get(str) != None):
                    querygrams[str] = grams.get(str)
                else:
                    querygrams[str] = 0

entropy = 0
for word in querygrams:
    if querygrams.get(word)!=0:
        entropy += querygrams.get(word)*math.log2(querygrams.get(word))

print('Perplexity = ', 2**(-entropy))
