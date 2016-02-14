import re

texts = open('test.csv').read()
texts_list = texts.split(';')

print(len(texts_list))

def tokenize(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens

all_tokens = tokenize(texts)
all_tokens = set(all_tokens)

texts_tokens = []
for t in texts_list:
    texts_tokens.extend(set(tokenize(t)))
print texts_tokens


print(len(texts_list))
def index(all_lemmas, texts_list):
    D = {}
    for word in all_lemmas:
        for ind, text in enumerate(texts_list):
            text_list = tokenize(text)
            if word in text_list:
                if word in D:
                    D[word] += ', '+str(ind)
                else:
                    D[word] = str(ind)
    return D


Dictionary = {}
Dictionary = index(all_tokens, texts_list)

print(Dictionary)

query = input('Enter a query: ')

query_tokenize = tokenize(query)

def search(query_token, dict):
    numbers = []
    for word in query_token:
        if word in dict:
            value = dict[word].split(', ')
            numbers.extend(value)
    if numbers:
        numbers = set(numbers)
    else:
        print('sorry, no matches')
    return numbers

answer = search(query_tokenize, Dictionary)

for i in answer:
    print(texts_list[int(i)])