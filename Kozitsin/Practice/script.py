# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 13:16:33 2016

@author: kelmomas
"""
import math
import locale
import sys
import codecs
import string
import re

MAX_COUNT = 35971

sys.stdout = codecs.getwriter('CP1251')(sys.stdout)
loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, '')

class Gramms:
    def __init__(self):
        self.first = ""
        self.second = ""
        self.third = ""
        
    def set(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third
    
    def toString(self):
        return self.first + ' ' + self.second + ' ' + self.third

def prepareText(text):
    regex = re.compile('[%s]' % re.escape(string.punctuation + string.digits))
    text = regex.sub(' ', text)
    words = text.split()
    return words

def removePunctuation(line):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    line = regex.sub(' ', line)
    record = line.split()
    return record
    
def check3Gramms(filename, obj):
    with open(filename, 'r') as file:
        for line in file:
            line = removePunctuation(line)
            if ((line[1] == obj.first) and (line[2] == obj.second) and (line[3] == obj.third)):
                file.close()            
                return float(line[0]) / MAX_COUNT
    file.close()
    return 0

f = open('workfile.txt', 'r')
words = prepareText(f.read())

obj = Gramms()

perplexity = 0.0
power = 0.0
for i in xrange(1, len(words) - 2):
    obj.set(words[i], words[i + 1], words [i + 2])    
    probability = check3Gramms('3grams-3.txt', obj)
    print probability
    if (probability != 0.0):
        power = power + probability * math.log(probability, 2)

perplexity = math.pow(2, -power)
print "perplexity: ", perplexity
f.close()    