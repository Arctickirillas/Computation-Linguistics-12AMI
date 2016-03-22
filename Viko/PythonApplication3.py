import locale
import sys
import codecs

import math
import re
import string


############################################################
sys.stdout = codecs.getwriter('CP1251')(sys.stdout)
loc=locale.getlocale()
locale.setlocale(locale.LC_ALL, '')
############################################################

def Threegrams():

    file = open ('3grams-3.txt', mode ='r') 
    for i in file:
        i = i[0:-1]
        words = i.split('\t')
        #print float(words[0])/MAX_COUNT
        gramma=''
        gramma = words[1] + ' ' + words[3] + ' ' + words[5]
        #print (words)
        threegrams[gramma] = float(words[0])/MAX_COUNT
        #print (threegrams)
        #print(words[0])

    file.close()
    return threegrams


def Mythreegrams():
    file = open ("1.txt", mode ='r')
    for i in file:
        i = i[0:-1]
        #regex = re.compile('[%s]' % re.escape(string.punctuation + string.digits + string.ascii_letters))
        #words = regex.sub('', words)
        words = i.split()  
        for j in range (len(words) - 2):
            gramma = words[j] + ' ' + words[j+1] + ' ' + words[j+2]
            for k in  threegrams:
                if (threegrams.get(gramma) != None):
                    mythreegrams[gramma] = threegrams.get(gramma)
                else:
                    mythreegrams[gramma] = 0
    file.close()
    return mythreegrams


#########################  main ################
MAX_COUNT = 35971
threegrams = dict()
threegrams = Threegrams()

mythreegrams = dict()
mythreegrams = Mythreegrams()
print (mythreegrams)

power = 0.0

for i in mythreegrams:
    if (mythreegrams.get(i) != 0):
        power = power + mythreegrams.get(i)*math.log(mythreegrams.get(i), 2)

perplexity = math.pow(2, -power)
print ("perplexity = ", perplexity)


############################################################
locale.setlocale(locale.LC_ALL, loc)