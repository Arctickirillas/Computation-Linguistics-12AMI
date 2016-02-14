__author__ = 'Gusev Ivan'

import pandas as pd
import numpy as np
import csv
import re
import traceback

input_file  = open('input_text.csv', 'rU')
input_file = csv.reader(input_file, delimiter = ';')

dictionary = set([])
tf = []
symbolsInspector = re.compile(r'[-.?!,\"\:;()\']')

for row in input_file:
    splittedLine =(symbolsInspector.sub('',row[1]).lower().split())
    #print(splittedLine)
    dictionary = dictionary.union(set(splittedLine))
    tf_i = dict(zip(dictionary,np.zeros(len(dictionary))))
    for word in splittedLine:
        if word in tf_i:
            tf_i[word] = 1.
    tf.append(tf_i)

dataFrameTF = pd.DataFrame(tf).fillna(0)
#print(dataFrameTF)
print('Enter the query:')
phrase = raw_input()
phrase = (re.split("[\s;:\-_*\".,?!()]", phrase))


print(dataFrameTF.get(phrase))
