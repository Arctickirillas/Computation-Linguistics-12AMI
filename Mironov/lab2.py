import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import re
from os import listdir

stop_symbols = re.compile(r'[-.?!#,\"\:;()\']|http[.:/a-zA-Z0-9]*|@[a-zA-z0-9]*|RT')

dictionary = set([])
positive = []
negative = []

bank_path = 'bank_train/'
file_list = listdir(bank_path)

for path in file_list:
    tree = ET.parse(bank_path+path)
    root = tree.getroot()
    for j,element in enumerate(root.iter('table')):
        line =(stop_symbols.sub('',element[4].text).lower().split())
        dictionary = dictionary.union(set(line))

        for i in range(0,8,1):
            if element[i+5].text == '1':
                tf = dict(zip(dictionary,np.zeros(len(dictionary))))
                for word in line:
                    if word in tf:
                        tf[word] += 1.
                positive.append(tf)
                break
            elif element[i+5].text == '-1':
                tf = dict(zip(dictionary,np.zeros(len(dictionary))))
                for word in line:
                    if word in tf:
                        tf[word] += 1.
                negative.append(tf)
                break

df_pos = pd.DataFrame(positive).fillna(0)
df_neg = pd.DataFrame(negative).fillna(0)

def get_r_i(statement):
    r_i = []
    for word in statement:
        if word in df_pos:
            r = sum(df_pos[word])
            r_i.append(r)
        else:
            r_i.append(0.)
    return r_i

def get_n_i(statement):
    n_i = []
    for word in statement:
        if word in pd.concat([df_pos,df_neg]):
            n = sum(df_pos[word]) + sum(df_neg[word])
            n_i.append(n)
        else:
            n_i.append(0.)
    return n_i

def get_c_i(r_i,R,n_i,N):
    c_i = []
    c = 0
    for i in range(len(r_i)):
        a = r_i[i]/R
        b = (n_i[i] - r_i[i])/(N - R)
        _c_i = np.log(((r_i[i]+0.5)/(R-r_i[i]+0.5))/((n_i[i]-r_i[i]+0.5)/(N-n_i[i]-R+r_i[i]+0.5)))
        c += np.log((1-a)/(1-b))
        c_i.append(_c_i)
    return c_i,c

# main
print('Make request:')
request = input()
request = stop_symbols.sub('',request).lower().split()

R = len(positive)
N = len(negative+positive)
c_i,c = get_c_i(get_r_i(request),R,get_n_i(request),N)
g_d = sum(c_i)+c

csv_file = open('out.csv', 'w')
for i,word in enumerate(request):
    csv_file.write(word+';'+str(c_i[i])+'\n')
csv_file.close()

if g_d > c:
    print('class:+1')
elif g_d < c:
    print('class:-1')
elif g_d == c:
    print('class:unknown')
print('g(d) = '+str(g_d))
