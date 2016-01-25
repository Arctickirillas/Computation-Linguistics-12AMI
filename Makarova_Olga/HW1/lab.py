import re
from pymystem3 import Mystem

texts = open('texts.csv').read()
texts_list = texts.split(';')

def tokenize(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens

all_tokens = tokenize(texts)
mystem = Mystem()
string = ' '.join(all_tokens)
def normalize(string):
    all_lemmas = mystem.lemmatize(string)
    all_lemmas = set(all_lemmas[::2])
    return all_lemmas

lemmas = normalize(string)

text_lemmas = []
for text in texts_list:
    sent_tokens = tokenize(text)
    sent_string = ' '.join(sent_tokens)
    sent_norm = normalize(sent_string)
    text_lemmas.append(sent_norm)

def index(all_lemmas, texts_lemmas):
    D = {}
    for word in all_lemmas:
        for ind, text in enumerate(texts_lemmas):
            if word in text:
                if word in D:
                    D[word] += ', '+str(ind)
                else:
                    D[word] = str(ind)
    return D

dict = index(lemmas, text_lemmas)

query = input('введите, пожалуйста, ваш запрос: ')

query_tokenize = tokenize(query)
query_tokenize = ' '.join(query_tokenize)
query_normalize = normalize(query_tokenize)

def search(query_normalize, dict):
    numbers = []
    for word in query_normalize:
        if word in dict:
            value = dict[word].split(', ')
            numbers.extend(value)
    if numbers:
        numbers = set(numbers)
    else:
        print('sorry, no matches')
    return numbers

answer = search(query_normalize, dict)

for i in answer:
    print(texts_list[int(i)])