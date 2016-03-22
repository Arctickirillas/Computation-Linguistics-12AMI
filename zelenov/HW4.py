# -*- coding: utf-8 -*-

import math

def take_3gram():
    with open ('3grams-3.txt','r',encoding='utf-8') as f:
        txt = f.read().split('\n')
        f.close()
    #print (txt)
    gram3 = dict({})
    for ln in txt:
        item = ln.split('\t')
        try:
            gram3[(item[1],item[3],item[5])]=float(item[0])/35971
        except:
            pass
    return gram3

texts = open("text.txt",encoding='utf-8')

gr = take_3gram()

#print(texts)

perplexity = 0.0
for text in texts:
    words = text.lower().split()

    for i in range(0,len(words)-2):
        if gr.get((words[i], words[i+1], words[i+2])):
            perplexity += gr[(words[i], words[i+1], words[i+2])] * math.log2(gr[(words[i], words[i+1], words[i+2])])
print(perplexity)
perplexity = math.pow(2,-perplexity)
print(perplexity)
