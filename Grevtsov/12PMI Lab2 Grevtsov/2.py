

import xml.etree as etree
import xml.etree.ElementTree as et
import re
import math


def to_tokens(text):
    text = text.lower()
    tokens = re.findall('\w+', text)
    return tokens

part1="bank (" #создаём первую часть имени файла
part2=").xml" #и вторую, для поочерёдного считывания файлов в цикле
the_text="" #переменная для хранения текстов всех твитов
relevant_class="" #для хранения id релевантных (с 1)
non_relevant_class="" #для хранения id не релевантных (с -1)
text_for_every_y_or_n_relevant={} #для хранения (не)релевантных текстов

for i in range (1,50):
    tree = et.parse(part1+str(i)+part2)
    root = tree.getroot()
    for child in root.iter('table'):
        the_text=the_text+child[4].text+" "
        flag=0
        for j in range (5,12):
            if child[j].text=="1":
                relevant_class=relevant_class+child[0].text+","
                flag=1
                text_for_every_y_or_n_relevant[child[0].text]=child[4].text.lower()#+","+str(flag)
                break
            else:
                if child[j].text=="-1":
                    non_relevant_class=non_relevant_class+child[0].text+","
                    flag=-1
                    text_for_every_y_or_n_relevant[child[0].text]=child[4].text.lower()#+","+str(flag)
                    break

tokens = set(to_tokens(the_text))


print(tokens)
"""
print(relevant_class)
print(non_relevant_class)
"""
relevant_class_list = set(relevant_class.split(','))
relevant_class_list.remove("")

non_relevant_class_list = set(non_relevant_class.split(','))
non_relevant_class_list.remove("")

print(relevant_class_list)
print(non_relevant_class_list)
print(text_for_every_y_or_n_relevant)
#print("amount of words in rel & non_rel texts: ",len(text_for_every_y_or_n_relevant))
print("number of rel & non_rel doc (N) :", len(relevant_class_list)+len(non_relevant_class_list))
print("number of relevant documents (R): ",len(relevant_class_list))
N=len(relevant_class_list)+len(non_relevant_class_list)
R=len(relevant_class_list)


#print(new_text)
mas1={} #сколько релевантных текстов содержащих слово (берутся только слова из релевантных и нерелевантных текстов, остальные не учитываются) (ri)
mas2={} #сколько нерелевантных текстов содержащих слово (ni-ri)
check={}
for word in tokens:
    mas1[word]=0
    mas2[word]=0
    check[word]=0


for word in tokens:
    for rel_index in relevant_class_list:
        new_text1=text_for_every_y_or_n_relevant[rel_index].split(" ")
        #print(new_text)
        for text in new_text1:
           if word==text:
            if check[word]!=1:
                mas1[word]+=1
                check[word]=1
        for text in new_text1:
            check[text]=0

    for non_rel_index in non_relevant_class_list:
        new_text2=text_for_every_y_or_n_relevant[non_rel_index].split(" ")

        for text in new_text2:
            if word==text:
                if check[word]!=1:
                    mas2[word]+=1
                    check[word]=1
                    #print(word,check[word])
                    #print("lol")
        for text in new_text2:
            check[text]=0

print("slova v relevantnbIh tekstah (ri): ",mas1)

"""
for word in mas1:
    if mas1[word]!=0:
        print(word,mas1[word])
"""
print("slova v NErelevantnbIh tekstah (ni-ri): ", mas2)
"""
for word in mas2:
    if mas1[word]!=0:
        print(word,mas2[word])
"""
ri=mas1
ni_minus_ri=mas2
ai={}
bi={}
for word in tokens:
    ai[word]=ri[word]/R
    bi[word]=ni_minus_ri[word]/(N-R)
print("_______________________")
print("ai: ",ai)
print("bi: ",bi)
ci={}
"""
for word in ai:
    if ai[word]==1:
        print (word, ai[word])
print("***********************")
for word in bi:
    if bi[word]==0:
        print(word, bi[word])
"""
for word in tokens:
    #ci[word]=math.log(ai[word]*(1-bi[word])/(bi[word]*(1-ai[word])))
    ci[word]=math.log(((ri[word]+0.5)/(R-ri[word]+0.5))/((ni_minus_ri[word]+0.5)/(N-R-ni_minus_ri[word]+0.5)))
print("ci: ",ci)
C=0
for word in tokens:
    C+=math.log((1-ai[word])/(1-bi[word]))
print("C: ",C)
G=0
count=0
for word in tokens:
    if ri[word]!=0:
        G+=ci[word]
        count+=1
G+=C
print("G: ",G)
print("count: ",count)











