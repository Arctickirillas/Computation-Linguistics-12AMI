# -- coding: utf-8 --
from lxml import etree
import re,string,math,sys
rel = {}
pos = 0
neg =0
for i in range (1,51):
    f=open('banks_train\\bank ('+str(i)+').xml','r')
    root = etree.parse(f)
    for table in root.getiterator('table'):
            for column in table:
                if (column.attrib.get("name")=="text"):
                    txt = column.text
                if (column.attrib.get("name") in ["sberbank","vtb","gazprom","alfabank","bankmoskvy","raiffeisen","uralsib","rshb"]):
                    if(column.text=="1"):
                        rel.update([(txt,1)])
                        pos+=1
                    if(column.text=="-1"):
                        rel.update([(txt,0)])
                        neg+=1
ab={}
rus = re.compile(u'[ёйцукенгшщзхъфывапролджэячсмитьбю][ёйцукенгшщзхъфывапролджэячсмитьбю]+')
for tweet,r in rel.items():
    for word in tweet.split():
        word = word.lower()
        exclude = set(string.punctuation)
        word = ''.join(ch for ch in word if ch not in exclude)
        if ab.has_key(word):
            if r==1:
                ab.update([(word,[ab.get(word)[0]+1,ab.get(word)[0]])])
            else:
                ab.update([(word,[ab.get(word)[0],ab.get(word)[0]+1])])
        else:
            if r==1:
                ab.update([(word,[1,0])])
            else:
                ab.update([(word,[0,1])])
for word,v in ab.items():
    if rus.match(word):
        ab.update([(word,[v[0]/float(pos)+sys.float_info.min,v[1]/float(neg)+sys.float_info.min])])
    else:
        ab.pop(word)
c={}
cnst = 0
for word,v in ab.items():
    c.update([(word,math.log(v[0]*(1-v[1])/v[1]/(1-v[0])))])
    cnst+=math.log((1-v[0])/(1-v[1]))
ans=cnst

result_file = open('coefficients.csv', 'w')
for word,ci in c.items():
    result_file.write(word.encode('utf-8') + ";")
    result_file.write(str(ci))
    result_file.write('\n')
result_file.write('\n C;' + str(cnst) + '\n')

query = 'Кипр Райффайзен банк кредит'
for qword in query.split(' '):
    qword = qword.lower()
    exclude = set(string.punctuation)
    qword = ''.join(ch for ch in word if ch not in exclude)
    ans+=c.get(qword)
print("Relevancy = "+ str(ans))