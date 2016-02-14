import re

file = open('text.csv', 'r')
open_file = file.read()
file.close()

def text_prep(text):
    """Preprocessing of the text"""
    text1 = text.lower()
    text2 = re.sub('[.,!?"\'-\\\/:;1-9+]', ' ', text1)
    text3 = text2.replace('\n', ' ')
    text4 = re.sub(' +', ' ', text3)
    text_obrab = text4.split()
    return text_obrab

texts = []
text_file = open_file.split(';\n')

for i in text_file:
    texts.append(text_prep(i))

voc = []
for i in texts:
    voc.extend(i)
vocc = set(voc)
voc.clear()
for i in vocc:
    voc.append(i)

list1=[]
list2=[]

for i in voc:
    for j in range(len(texts)):
        for k in texts[j]:
            if i==k:
                list1.append(j)
                break
    list2.append(list1[:])
    list1.clear()
#print(list2) #inverted index

def print_str(dict, index ):
    for i in range(len(dict)):
        print(dict[i],'=',index[i])

#print_str(voc, list2 )

query = input("enter your query: ")
#query = "Man and cat"

if query=='':
    print('The data is entered incorrectly')
else:
    query = text_prep(query)
    print(query)

    result=[]
    for i in query:
        for k in range(len(voc)):
                if i == voc[k]:
                    result.append(list2[k])

    print(result)
    print('Specified words are in text(s):')
    print_str(query, result)


