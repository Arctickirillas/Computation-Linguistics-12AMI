__author__ = 'Kirill Rudakov'

import csv
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import re
import numpy as np
from scipy.sparse import csr_matrix
import pickle
class InvertedIndex:
    # file: path to file; language: current articles language; searchingType: use numbers for searching or not
    def __init__(self, file = '/Rudakov Kirill/HW1/ENGtext.csv',language = 'english', searchingType = 'withNumbers'):
        self.file = file
        self.language = language
        if searchingType == 'withNumbers':
            self.recursion = re.compile(r'[-.?!,\"\:;()\']') # withNumbers
        else:
            self.recursion = re.compile(r'[-.?!,\"\:;()\'|0-9]') # withoutNumbers

        self.numberOfText = 0

    def obtainOrRebuildIndex(self):
        def makeFullMatrix(rowIndex,indexLabel):
            for i in (range(len(indexLabel)-len(rowIndex))):
                rowIndex.append(0)
        # temp vars
        _indexLabel = []
        _rowIndex = []
        _listOfRow = []
        # simple stemmer
        self.stemmer = SnowballStemmer(self.language)
        # open csvfile and obtain the data
        with open(self.file,'rt') as csvfile:
            spreadshit = csv.reader(csvfile, delimiter=';', )
            for t,row in enumerate(spreadshit):
                if t==0:
                    self.header = list(row)
                else:
                    self.numberOfText +=1
                    _rowIndex = [0]*len(_rowIndex)
                    _label = word_tokenize(list(row)[0])
                    _article = word_tokenize(list(row)[1])
                    _text = _label + _article

                    for i,token in enumerate(_text):
                        s = self.stemmer.stem(token)
                        s = self.recursion.sub('',s)
                        if s != '' and s not in _indexLabel:
                            _indexLabel.append(s)
                            _rowIndex.append(1)
                        elif s in _indexLabel:
                            _rowIndex[_indexLabel.index(s)] += 1
                    _listOfRow.append(_rowIndex)
                    del _label,_article,_text
            csvfile.close()

        for i in range(self.numberOfText):
            makeFullMatrix(_listOfRow[i],_indexLabel)

        self.indexLabel = _indexLabel
        self.index = (csr_matrix(_listOfRow))

        del _listOfRow,_rowIndex,_indexLabel

    def toFind(self,phrase):
        def toStem(phrase):
            _newStatement = []
            phrase = word_tokenize(phrase)
            for i,token in enumerate(phrase):
                        s = self.stemmer.stem(token)
                        _newStatement.append(s)
            return _newStatement

        def toDisplay(table,i = 1):
            i = i
            with open(self.file,'rt') as csvfile:
                spreadshit = csv.reader(csvfile, delimiter=';', )
                query = list(spreadshit)[table[-i]+1]
                print('\n'+self.header[0]+':',query[0],'\n'+self.header[1]+':',query[1])

        # id, countOfMatch, sum
        def sortTable(table):
            _newTable = []
            dtype = ([('id', float), ('count', float), ('sum', float)])
            for i in range(table.shape[0]):
                _sum = 0
                _count = 0
                for j in range(table.shape[1]):
                        if table[i][j] != 0:
                            _count += 1
                        _sum += table[i][j]
                _newTable.append((i,_count,_sum))

            _newTable = np.array(_newTable)
            _newTable.dtype = dtype
            _newTable = (np.sort(_newTable,order=['count', 'sum'],axis=0,kind='heapsort'))

            table = []

            for i in range(len(_newTable)):
                if int(_newTable[i][0][2])>0:
                    table.append(int(_newTable[i][0][0]))
            return table

        phrase = toStem(phrase)
        table = np.zeros((self.numberOfText,len(phrase)))
        for w,word in enumerate(phrase):
            for i in range(self.numberOfText):
                try:
                    element = self.index.getrow(i).getcol(self.indexLabel.index(word))
                    if element>0:
                        table[i][w] = element.toarray()[0][0]
                except Exception:
                    print('Searching without','\"'+word+'\"')
                    break

        table = sortTable(table)
        # print(table)
        it = 1

        toDisplay(table,it)
        print('\nType \'Next\' or \'Prev\' to see more.'
              '\nOtherwise - exit')
        inputPhrase = input()
        while True:
            if inputPhrase=='Next':
                try:
                    toDisplay(table,it+1)
                    it += 1
                except IndexError:
                    print('End of the list')
            elif inputPhrase=='Prev':
                if it-1 <= 0:
                    print('End of the list')
                    it =0
                else:
                    it -=1
                    toDisplay(table,it)
            else:
                break
            inputPhrase = input()

def main():
    print('Hello! This is implementation of inverted index.'
          '\nPlease, type a phrase to find it in corpus:')
    # filePath = 'ENGtext.csv'
    ind = InvertedIndex()

    try:
        with open('/Rudakov Kirill/HW1/index.pickle', 'rb') as dump:
            ind.index = pickle.load(dump)
    except FileNotFoundError:
        ind.obtainOrRebuildIndex()
        with open('/Rudakov Kirill/HW1/data.pickle', 'wb') as dump:
            pickle.dump(ind.index, dump)
    inputPhrase = input()

    try:
        ind.toFind(inputPhrase)
    except Exception:
        print('Not found')

# -- Main
main()





