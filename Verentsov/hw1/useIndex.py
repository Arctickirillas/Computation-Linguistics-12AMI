import csv
search = "not sitting"
dictionary = {}
reader = csv.reader(open("index.csv","rb"))
for row in reader:
    dictionary[row[0]]=map(int,row[1:])
    dictionary[row[0]] = set(dictionary[row[0]])
textIndeces = {}
for word in search.split():
    word=''.join(e for e in word if e.isalnum())
    if(dictionary.has_key(word)):
        if(textIndeces=={}):
            textIndeces = dictionary[word]
        else:
            textIndeces = textIndeces & dictionary[word]
    else:
        print "Not found"
textIndeces = list(textIndeces)
print textIndeces
with open('collection.csv','r') as f:
    for i,line in enumerate(f):
        if i == textIndeces[0]:
            print line
            textIndeces.pop(0)
        if len(textIndeces)==0:
            break
