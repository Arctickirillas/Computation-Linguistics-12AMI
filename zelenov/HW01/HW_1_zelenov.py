import string
import lxml.html as html
import time
import pickle
import re

text = open('text.csv').read()
texts = text.split('\n')
# create index
dictionary = dict()
index = 0
delete = re.compile('[%s]' % re.escape(string.punctuation))
for text in texts:
    text = delete.sub(' ', text)
    words = text.split()
    for word in words:
        if (dictionary.get(word.lower()) == None):
            dictionary[word.lower()] = set()
        dictionary[word.lower()].add(index)
    index += 1

# search function

def search(words):
        if(dictionary.get(words[0])==None):
            print("error")
        else:
            result = dictionary[words[0]]
            for word in words:
                result = result.intersection(set(dictionary[word]))
                #print(result)
            return result


words = ["my","drag","feel"]
print(search(words))
print (dictionary)