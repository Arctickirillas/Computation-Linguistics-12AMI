import math
import re
import string


def Threegrams():

    with open('3grams-3.txt', 'r') as file:
        txt = file.read().split('\n')
        file.close()
    max = txt[0].split('\t')[0]
    for line in txt:
        item = line.split('\t')
        try:
            gram3[(item[1],item[3],item[5])] = int(item[0])/int(MAX_COUNT)
        except:
            pass
    return gram3


def Mythreegrams():
    file = open ("test.txt", 'r')
    for i in file:
        i = i[0:-1]
        words = i.split()  
        for j in range (len(words) - 2):
            gramma = words[j] + ' ' + words[j+1] + ' ' + words[j+2]
            for k in  gram3:
                if (gram3.get(gramma) != None):
                    mythreegrams[gramma] = gram3.get(gramma)
                else:
                    mythreegrams[gramma] = 0
    file.close()
    return mythreegrams


#########################  main ################
MAX_COUNT = 35971
gram3 = {}
gram3 = Threegrams()

mythreegrams = dict()
mythreegrams = Mythreegrams()
print (mythreegrams)

power = 0.0

for i in mythreegrams:
    if (mythreegrams.get(i) != 0):
        power = power + mythreegrams.get(i)*math.log(mythreegrams.get(i), 2)

perplexity = math.pow(2, -power)
print ("perplexity = ", perplexity)


