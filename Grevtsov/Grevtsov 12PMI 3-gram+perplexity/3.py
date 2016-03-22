# -*- coding: utf-8 -*-
import math

def get_text():
    f= open('text.txt','r',encoding='utf-8')
    text = [f.read()]
    print(text)
    text=f.read()
    f.close()
    return text

def make_3gram():
    with open ('3grams-3.txt','r',encoding='utf-8') as f:
        txt = f.read().split('\n')
        f.close()
    gram3 = dict({})
    for words in txt:
        w = words.split('\t')
        try:
            gram3[(w[1],w[3],w[5])]=float(w[0])/35971
        except:
            pass
    return gram3

texts = get_text()
print(texts)
perplexity = 0.0
gr = make_3gram()
for text in texts:
    w = text.lower().split()
    for i in range(0,len(w)-2):
        if gr.get((w[i], w[i+1], w[i+2])):
            perplexity += gr[(w[i], w[i+1], w[i+2])] * math.log2(gr[(w[i], w[i+1], w[i+2])])
print(perplexity)
perplexity = math.pow(2,-perplexity)
print(perplexity)