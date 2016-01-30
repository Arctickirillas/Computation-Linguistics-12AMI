
from functools import reduce

def parsetexts(file = '1.csv'):
    texts = []
    words = set()
    with open(file, 'r') as f:
            txt = f.read()
            stre= txt.split("\n")
            txt = txt.split()
            for line in txt:
                word = line.split(",")
                #print (word)
            words |= set(txt)
            texts.append(stre)
    return texts, words


texts, words = parsetexts()
print ('\nTexts')
print (texts)
print('\nWords')
print (words)

def invindex():
    diction = dict()
    i = 0
    for line in texts:
        #print(line)
        for word in line:
            #print(word)
            word = word.split()
            for w in word:
                #print(w)
                if diction.get(w) == None:
                    diction[w] = []
                diction[w].append(i)
            i = i + 1
    return diction
diction = invindex()
print ('\nInvIndex')
print (diction)

def search(terms):
     if diction.get(terms[0]) == None:
         print ('\nError!')
         exit(-1)
     result = set(diction[terms[0]])
     for word in terms:
         result = result.intersection(set(diction[word]))
     return result

terms = ["старик","со"]
print('\nSearch for: ' + repr(terms))
end = search(terms)
for k in end:
    print(texts[0][k])