# coding=utf-8
import codecs

import lxml.etree as ET
from zipfile import *
import re
import string
import locale
import numpy

import sys
from pymystem3 import Mystem

def tokenize(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens

name_list = []
if is_zipfile('../../banks_train.zip'):
    z = ZipFile('../../banks_train.zip', 'r')
    z.extractall()
    name_list = z.namelist();
    z.close()
#print(name_list)

list_tvits = []
list_rel_tvits = []
list_null_tvits = []
list_nonrel_tvits = []
texts = []
labels = []

for name in name_list:
    tree=ET.parse(name)
    root=tree.getroot()
    for element in root.iter('table'):
        list_tvits.append(element[4].text)
        for i in range(5, 12):
			if(element[i].text == '1'):
				texts.append(element[4].text)
				labels.append(1)
				break
			elif(element[i].text == '-1'):
				texts.append(element[4].text)
				labels.append(0)
				break
#print(labels)

regex = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters + string.digits))
temp = []
for text in texts:
    temp.append(re.sub(regex, '', text))

all_tokens = set(temp)

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
#print(text_lemmas)

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

ci = []
C = 0
for ind, lemma in enumerate(lemmas):
    C += numpy.log((1-(ri_list[ind]/R))/(1-((ni_list[ind]-ri_list[ind])/(N-R))))
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