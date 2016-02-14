# coding=utf-8
import re
from pymystem3 import Mystem
import numpy
import lxml.etree as ET
from zipfile import *

def tokenize(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens



texts = [('я слушаю всякую разную музыку, гранж, например, потому что он крут и атмосферен', 1),
         ('ты слышал новый альбом этой певицы? он какой-то мерзкий: странные мелодии, визгливый вокал', 1),
         ('я опять влюбился, чувак, больше не могу уже', 0),
         ('машины - это лучшее, что я умею делать', 0),
         ('я больше не занимаюсь продвижением их группы, теперь они сами по себе, теперь они сами пишут песни и мастерят альбомы', 1),
         ('синий - отличный цвет для твоей новой картины, мне кажется', 0),
         ('самолёт опять разбился в городе, сколько уже можно', 0),
         ('ты идешь на их выступление? пойдём, там будет весело', 0)
]

temp = [a[0] for a in texts]
labels = [a[1] for a in texts]
all_tokens = tokenize(' '.join(temp))
mystem = Mystem()
string = ' '.join(all_tokens)

def normalize(string):
    all_lemmas = mystem.lemmatize(string)
    all_lemmas = set(all_lemmas[::2])
    return all_lemmas

lemmas = set(normalize(string))
text_lemmas = []
for text in temp:
    sent_tokens = tokenize(text)
    sent_string = ' '.join(sent_tokens)
    sent_norm = normalize(sent_string)
    text_lemmas.append(sent_norm)

#vectors = []
ni_list = []
ri_list = []
R = labels.count(1)
N = len(labels)

for lemma in lemmas:
    counter_n = 0
    counter_r = 0
    for ind, text in enumerate(text_lemmas):
        if lemma in text:
            if labels[ind] == 1:
                counter_r += 1
            counter_n += 1
    ni_list.append(counter_n)
    ri_list.append(counter_r)

"""for ind, text in enumerate(text_lemmas):
    vector = []
    for lemma in lemmas:
        if lemma in text:
            vector.append(1)
        else:
            vector.append(0)
    vectors.append(vector)"""

ci = []
C = 0
for ind, lemma in enumerate(lemmas):
    C += numpy.log((1-(ri_list[ind]/R))/(1-((ni_list[ind]-ri_list[ind])/(N-R))))
    #smoothing is implemented
    ci_num = numpy.log(((ri_list[ind] + 0.5)/(R - ri_list[ind] + 0.5))/((ni_list[ind] - ri_list[ind] + 0.5)/(N - ni_list[ind] - R + ri_list[ind] + 0.5)))
    ci.append(ci_num)

input_text = input('type smth: ')
input_text = set(normalize(input_text))
vector = []

for lemma in lemmas:
    if lemma in input_text:
        vector.append(1)
    else:
        vector.append(0)


X = []
for i in range(len(vector)):
    if vector[i] == 0:
        X.append(1-((ni_list[i]-ri_list[i])/(N-R)))
    else:
        X.append(1-(ri_list[ind]/R))

g_function = 0
for i in range(len(X)):
    g_function += ci[i] * X[i] + C

print(g_function)
"""
3)приходит новый текст(документ) . ты считаешь функцию для него g(d) = ci*xi +C.
Вот и навыходе он хочет табличку
слово - вес(ci)
и в конце просто еще С(это вес всего текста вроде как) вписываешь и все.

ni: number of documents with term ti
ri: number of relevant documents with term ti
R: number of relevant documents
N: number of documents

g(d) = ci*xi +C
ai = ri/R
bi = ni-ri/N-R
ci = log(ri/(R-ri)//(ni-ri)/(N-ni-R+ri)
((ri + 0.5)/(R − ri + 0.5))
((ni − ri + 0.5)/(N − ni − R + ri + 0.5))
P(< 0, 1, 1, 0, 0, 1 > |r) = (1 − a1) · a2 · a3 · (1 − a4) · (1 − a5) · a6
P(< 0, 1, 1, 0, 0, >)|¬r) = (1 − b1) · b2 · b3 · (1 − b4) · (1 − b5) · b6
"""