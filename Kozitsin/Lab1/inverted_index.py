# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:00:38 2016

@author: kelmomas
"""

import scipy.sparse as sci
import csv
import sys
import warnings

warnings.filterwarnings("ignore")

def buildIndex(path):
    try:
        mapping = dict() # to keep mapping between word and row in matrix 
        row = list() # list to store row indexes
        col = list() # list to store col indexes
        data = list() # list to store bool value
        
        with open(path, 'rb') as csvfile:
            textReader = csv.reader(csvfile, delimiter=' ')
            
            i = 0 # keep amount of words
            j = 0 # keep amount of texts
            
            for rows in textReader: 
                for cell in rows:
                    if cell in mapping: # means we already had this word
                        current = mapping.get(cell) # get a row of matrix
                        
                        row.append(current)
                        col.append(j)
                        data.append(1)
                    else:
                        row.append(i)
                        col.append(j)
                        data.append(1)
                        mapping.update({cell : i})
                        
                        i = i + 1 # increment word number
                        
                j = j + 1 # increment text number
        
        # build coo matrix and convert to csr 
        indexes = sci.coo_matrix((data, (row, col)),
                                  shape = (i, j))
                                 
        return (mapping, indexes.tocsr(), j)
    except:
        print "Error appeared: ", sys.exc_info()[0]
        return None

def retrieveSet(i, invIndex):
    try:
        indexSet = set()
        row = invIndex.getrow(i).nonzero() # get matrix of nonzero elements
                                           # positions
        for col in row[1]:                 # get columns
            indexSet.add(col)
        return indexSet
    except:
        print "Error appeared: ", sys.exc_info()[0]
        return None
            
def initSet(numOfTexts):
    filterSet = set()
    
    for i in xrange(0, numOfTexts):
        filterSet.add(i)
        
    return filterSet
    
def extSearch(phrase, mapping, invIndex,numOfTexts):
    try:    
        words = phrase.split(" ")
        filterSet = initSet(numOfTexts) # final result
        
        for word in words:
            if (word in mapping):
                current = mapping.get(word)                
                filterSet = filterSet.intersection(retrieveSet(current,
                                                               invIndex))
            else:
                filterSet = set()
        return filterSet
    except:
        print "Error appeared: ", sys.exc_info()[0]
        return None
        
def readFromCSV(path, result):
    try:
        with open(path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter = ' ')
            for i in xrange(0, len(result)):
                j = 0 # nmbr of already readed
                csvfile.seek(0)
                for row in reader:
                    if (result[i] == j):
                        print result[i], ':', ' '.join(row)
                        break
                    else:
                        j = j + 1
    except:
        print "Error appeared: ", sys.exc_info()[0]
        return None
    
def writeRawTexts(path, result):
    try:
        if (len(result) == 0):
            print "Nothing was found"
        else:
            print "phrase was found in texts below: ", result
            readFromCSV(path, result)
    except:
        print "Error appeared: ", sys.exc_info()[0]
        
        
###########################################################
#                      MAIN BLOCK                         #
###########################################################        
print("This is python script for building inverted index.")
print("Algo do not pay attention to stop-symbols.")
print("Space considered as delimiter.")

path = raw_input("Please, specify collection of text in *.csv format: ")
phrase = raw_input("Please, enter phrase for search: ")

mapping, invIndex, numOfTexts = buildIndex(path)
result = list(extSearch(phrase, mapping, invIndex, numOfTexts))

writeRawTexts(path, result)
###########################################################
#                                                         #
########################################################### 