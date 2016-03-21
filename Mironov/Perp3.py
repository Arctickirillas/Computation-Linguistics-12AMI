__author__ = 'Mironov Alexander'
import pickle
import math

def getGram3():
    with open('3grams-3.txt','r') as file:
        txt = file.read().split('\n')
        file.close()
    max = txt[0].split('\t')[0]
    gram3 = {}
    for line in txt:
        item = line.split('\t')
        try:
            gram3[(item[1],item[3],item[5])] = int(item[0])/int(max)
        except:
            pass
    return gram3

texts  = open('text.txt','r')
texts = texts.read().split('\n')

gr = getGram3()
perSum = 0
for text in texts:
    words = text.lower().split()
    if len(words)>2:
        for i in range(len(words)-2):
            if (words[i],words[i+1],words[i+2]) in gr:
                p = gr[words[i],words[i+1],words[i+2]]
                perSum +=  p*(math.log(p))
perplexity = 2**(-1*perSum)
print(perplexity)
