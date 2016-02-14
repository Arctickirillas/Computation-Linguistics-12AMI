# coding=utf-8
import re
from pymystem3 import Mystem

def tokenize(text):
    tokens = re.findall('\w+', text)
    return tokens

"""texts = open(text)
    a = texts.read()
    texts.close()
"""
structure = open('new_bank.xml', encoding='utf-8')
file = structure.read()
structure.close()
file = file.lower()
#creating lists of rus words and string form of them for further lemmatization
words = re.findall('[а-я]+', file)
words_str = ' '.join(words)

#extracting tweets and labels from the text
lines = file.split('\n')
strings = []
labels = []
temporal = []
for i in range(0, len(lines)):
	if lines[i].find('<column name="text">') != -1:
		temporal.append(lines[i])
	if temporal:
		if lines[i].find('>0<') != -1:
			temporal.append('0')
		elif lines[i].find('>-1<') != -1:
			temporal.append('-1')
		elif lines[i].find('>1<') != -1:
			temporal.append('1')
		if len(temporal) == 2:
		    strings.append(temporal[0])
		    labels.append(temporal[1])
		    temporal = []

#lemmatization
mystem = Mystem()
lemmas_norm = list(set(mystem.lemmatize(words_str)))

#cleaning up the sentences
rus_symbols = re.compile('[а-я]|\s')
text = ''

for string in strings:
	for symbol in string:
	    if rus_symbols.search(symbol):
		    text += symbol
	text += '. '

sentences = text.split('. ')

for i in range(len(sentences)):
    sentences[i] = sentences[i].strip()

#sentence lemmatizing
sentences_set = []
for i in range(0, len(sentences)):
	lemmas = set()
	sent = tokenize(sentences[i])
	for token in sent:
		lemmas.add(morph.parse(token)[0].normal_form)
	sentences_set.append(' '.join(lemmas))

"""lemmatized_sents_txt = open('lemmatized_sents.txt', 'w', encoding='utf-8')
temporal = '\n'.join(sentences_set)
lemmatized_sents_txt.write(temporal)
lemmatized_sents_txt.close()

parameters_txt = open('parameters.txt', 'w', encoding='utf-8')
temporal = '\n'.join(parameters)
parameters_txt.write(temporal)
parameters_txt.close()

labels_txt = open('labels.txt', 'w', encoding='utf-8')
temporal = '\n'.join(labels)
labels_txt.write(temporal)
labels_txt.close()"""