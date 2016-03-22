import math

def getGram3():
    with open('3grams.txt','r', encoding='UTF-8') as file:
        txt = file.read().split('\n')
        file.close()
    max = txt[0].split('\t')[0]
    gram3 = dict()
    for line in txt:
        item = line.split('\t')
        try:
            gram3[(item[1],item[3],item[5])] = float(item[0])/int(max)
        except:
            pass
    return gram3

texts = open('text.txt','r')
texts = texts.read().split('\n')

gr = getGram3()

text_3gram = dict()
for text in texts:
    words = text.lower().split()
    if len(words)>2:
        for i in range(len(words)-2):
            for j in gr:
                    if (gr.get((words[i], words[i+1], words[i+2])) is not None):
                        text_3gram[(words[i], words[i+1], words[i+2])] = gr.get((words[i], words[i+1], words[i+2]))
                    else:
                        text_3gram[(words[i], words[i+1], words[i+2])] = 0
#print(text_3gram)

k=0
file = open('Result.csv', 'w')
for s in text_3gram:
    file.write(str(s)+';')
    file.write(str(text_3gram.get(s)))
    file.write('\n')
    if text_3gram.get(s) != 0:
        k +=text_3gram.get(s)*math.log(text_3gram.get(s),2)
Perplexity = 2**(-k)
print(Perplexity)
file.write('Perplexity = ')
file.write(str(Perplexity))
file.write(';')
file.write('\n')
file.close()