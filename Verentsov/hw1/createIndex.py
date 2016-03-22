import csv
dictionary={}
with open('collection.csv','r') as f:
    i=0
    for line in f:
        for word in line.split():
            word=''.join(e for e in word if e.isalnum())
            word = word.lower()
            if (word!='') & dictionary.has_key(word):
                if(dictionary[word][-1]!=i):
                    dictionary[word].append(i)
            else:
                dictionary[word]=[i]
        i+=1
writer = csv.writer(open('index.csv', 'wb'))
for key, value in dictionary.items():
   writer.writerow([key]+value)




