import math

texts = open("texts.txt")

def take_3gram():
    with open ('3grams-3.txt', mode='r', encoding='utf-8') as f:
        txt = f.read().split('\n')
        f.close()
    gram3 = dict()
    for ln in txt:
        item = ln.split('\t')
        try:
            gram3[(item[1],item[3],item[5])]=float(item[0])/35971
        except:
            pass
    return gram3

gr = take_3gram()

my_3gram = dict()
for text in texts:
    words = text.lower().split()
    for i in range(len(words)-2):
        for j in gr:
                if (gr.get((words[i], words[i+1], words[i+2])) is not None):
                    my_3gram[(words[i], words[i+1], words[i+2])] = gr.get((words[i], words[i+1], words[i+2]))
                else:
                    my_3gram[(words[i], words[i+1], words[i+2])] = 0
print(my_3gram)

l = 0
file = open('answer.csv', 'w')
file.write('si')
file.write(';')
file.write('P(si)')
file.write('\n')
for s in my_3gram:
    file.write(str(s)+';')
    file.write(str(my_3gram.get(s)))
    file.write('\n')
    if my_3gram.get(s) != 0:
        l = l + my_3gram.get(s)*math.log(my_3gram.get(s), 2)
Perplexity = 2**(-l)
print(Perplexity)
file.write('Perplexity = ')
file.write(str(Perplexity))
file.write(';')
file.write('\n')
file.close()
