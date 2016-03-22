import re

texts = open('text_eng.csv').read()
texts_list = texts.split(';')
print(texts_list) #check
print(len(texts_list))#why 11 when it is 10 I don't understand, maybe it is eof, but nvm

def to_tokens(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens

tokens = set(to_tokens(texts)) #find all unique words
print(tokens) #check

def make_index(tokens,texts_list): #make indexed dictionary
    Dictionary={}
    for word in tokens: #for every word in tokens for all
        for ind, text in enumerate(texts_list): #for every text
            text_list=to_tokens(text) #make own tokens
            if word in text_list: #if the word in this text tokens
                if word in Dictionary: #if the word in dictionary
                    Dictionary[word] += ','+str(ind) #add index for the word
                else:
                    Dictionary[word] = str(ind) #else make it
    return Dictionary

D=make_index(tokens,texts_list)
print(D) #check

query=input("Input a query: ")

def find_texts(query_tokens, Dictionary):
    numbers=[]
    for word in query_tokens:
        if word in Dictionary:
            value=Dictionary[word].split(',')
            numbers.extend(value)
            if numbers:
                numbers=set(numbers)
            else:
                print("No matches found")
    return numbers

print(find_texts(to_tokens(query),D)) #answer in indexes
for i in find_texts(to_tokens(query),D):
    print(texts_list[int(i)]) #answer in texts









