# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:33:45 2016

@author: kelmomas
"""
    
def levensteinDistance(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    return min(levensteinDistance(a[1:], b[1:]) + (2 if a[0] != b[0] else 0),
               levensteinDistance(a[1:], b) + 1,
               levensteinDistance(a, b[1:]) + 1)

 
str1 = raw_input("Enter first string: ")
str2 = raw_input("Enter second string: ")

print "The Levenstein Distance: ", levensteinDistance(str1, str2)