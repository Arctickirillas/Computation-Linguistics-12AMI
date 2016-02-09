import string
import re
import csv

def UpgradeStr(row):
    row = row.lower()
    row = row.strip()
    row = re.sub(r'[,.?:/!-]', '', row)
    row = row.split()  
    return row  

def CreateIndex():
    mapping = dict()
    val = list()

    Treader = open("test.csv", "rb")
    j = 0 #number of str
    for row in Treader.readlines():
        row = UpgradeStr(row)
        #print row
        #print len(row)
        for i in xrange(0, len(row)):
            if (mapping.get(row[i]) == None):
                val.append([j])
                mapping[row[i]] = val
            else:
                val = mapping.get(row[i])
                val.append([j])
                mapping[row[i]] = val                
            val = list()
        j = j + 1
    return mapping

def Result(index):
    print ("These proposals include the original phrase:")
    with open("test.csv", "rb") as csv_fh:
        Treader = csv.reader(csv_fh, delimiter =',')
        for i in xrange(0, len(index)):
            csv_fh.seek(0)
            j = 0    
            for row in Treader:
                if (j == index[i][0]):
                    print row
                j = j + 1

def PreparePhrase():
    phrase = raw_input("Please enter the phrase")
    phrase = UpgradeStr(phrase)
    return phrase

#########   main   ###############
mapping = CreateIndex()
phrase = PreparePhrase()

if (len(phrase) == 0):
    print ("You have not entered phrase!")

elif (len(phrase) == 1):
    if (mapping.get(phrase[0]) != None):
        index = mapping.get(phrase[0])
        Result(index)
    else:
        print ("There is no such phrase")   
###########################################
else:
    br = 0
    if (mapping.get(phrase[0]) != None):
        index = mapping.get(phrase[0])
    else:
        br = -1
    if (br != -1): 
        for i in xrange(1, len(phrase)):
            a = index
            index = list()
            if (mapping.get(phrase[i]) != None):
                b = mapping.get(phrase[i])
            else:
                print ("There is no such phrase")
                break  
            for j in xrange(0, len(a)):
                for k in xrange(0, len(b)):
                    if (a[j] == b[k]):
                        index.append(a[j])
        Result(index)
    else:
        print ("There is no such phrase")
                      
        
        
    
            
          