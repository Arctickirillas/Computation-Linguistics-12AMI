__author__ = '315-10'
# import pymorphy2
# morph = pymorphy2.MorphAnalyzer()
# m = morph.parse('стали')
# print(m[0])
import math

texts = open("texts.txt", 'r')
def take_3gram():
    with open ('3grams-3.txt','r',encoding='utf-8') as f:
        txt = f.read().split('\n')
        f.close()

    gram3 = dict({})
    for ln in txt:
        item = ln.split('\t')
        try:
            gram3[(item[1],item[3],item[5])]=float(item[0])/35971
        except:
            pass
    return gram3

gr = take_3gram()
perplexity = 0.0

for text in texts:
    words = text.lower().split()

    for i in range(0,len(words)-2):
        if gr.get((words[i], words[i+1], words[i+2])):
            perplexity = perplexity + gr[(words[i], words[i+1], words[i+2])] * math.log2(gr[(words[i], words[i+1], words[i+2])])
perplexity = math.pow(2,-perplexity)
print(perplexity)