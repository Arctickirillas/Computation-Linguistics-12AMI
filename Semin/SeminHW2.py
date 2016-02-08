import xml.etree.ElementTree as et
import re
import string
import math

start = "banks/bank ("
end = ").xml"
regex = re.compile('[%s]' % re.escape(string.punctuation+string.ascii_letters+'«»'+string.digits+'–…'))
dicr = dict({})
dicall = dict({})
index = 0
for i in range(1, 51):
    result = start + str(i) + end
    tree = et.parse(result)
    root = tree.getroot()
    for child in root.iter('table'):
        for j in range(1, 9):
            if(child[4 + j].text == '1'):
                # means relevant text
                text = (str(regex.sub(' ', str(child[4].text)))).split()
                for word in text:
                    if(dicr.get(word) is None):
                        dicr[word] = set()
                    dicr[word].add(int(child[0].text))
                    if(dicall.get(word) is None):
                        dicall[word] = set()
                    dicall[word].add(int(child[0].text))
                break
            else:
                if(child[4 + j].text == '-1'):
                    # means irrelevant text
                    text = regex.sub(' ', str(child[4].text)).split()
                    for word in text:
                        if dicall.get(word) is None:
                            dicall[word] = set()
                        dicall[word].add(int(child[0].text))
                    break
        index += 1


ci = dict({})
r = len(dicr)
n = len(dicall)
c = 0
for word in dicall:
    if dicr.get(word) is not None:
        ri = len(dicr[word])
        ai = ri/r
        ni = len(dicall[word])
        bi = (ni - ri)/(n-r)
        ci[word] = math.log2(((ri+0.5)/(r-ri+0.5))/((ni-ri+0.5)/(n-ni-r+ri+0.5)))
        c += (math.log2((1-ai)/(1-bi)))

print(ci)
f = open('result.csv', 'w')
for word in ci:
    f.write(word+';')
    f.write(str(ci[word]))
    f.write('\n')
f.write('\nC;'+str(c)+'\n')
f.close()
s = input('Enter the line\n')
s = re.split('\.| |,|;', s)

result = c
for word in s:
    if ci.get(word) is not None:
        result += ci[word]
print(result)
