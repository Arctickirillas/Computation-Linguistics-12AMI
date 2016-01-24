#!/usr/bin/env python 
# -*- coding: utf-8 -*-

def print_line(index, filename):
    lines = 0
    for i in open(filename):
        i = i[0:-1]
        lines += 1
        if (lines == index):
            print(i)

def make_inv_index(filename):
    dictionary = dict()
    no_line = 0
    for i in open(filename):
        i = i[0:-1]
        words = i.split()
        no_line += 1
        for word in words:
            #lines.append(dictionary.get(word))
            if dictionary.get(word) == None:
                dictionary[word]= set()
                dictionary[word].add(no_line)
            else:
                dictionary[word].add(no_line)
    #print (dictionary)
    return dictionary

def find_me_in_text(input, filename):
    words = input.split()
    dictionary = make_inv_index(filename)
    lines = []
    if len(words)==1:
        lines = dictionary[words[0]]
    else:
        i = 0
        while i<len(words)-1:
            lines = set(dictionary[words[i]]) & set(dictionary[words[i+1]])
            i+=1
    if lines!= None:
        for index in lines:
            print_line(index, filename)
    else:
        print('None in this texts')

find_me_in_text('что','sherlock.csv')
