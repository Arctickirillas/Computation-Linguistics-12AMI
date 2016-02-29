from lxml import etree
from zipfile import *
import re
import string
import math

is_zipfile('banks_train.zip')
z = ZipFile('banks_train.zip', 'r')
z.extractall()
names = z.namelist()
#print(names)
tree = etree.parse(names[1])
print (tree)

hash = []
line_num = 1
lines = []
lines_rel = []
line = []
wella = []
hash_rel = []


for name in names:
     tree = etree.parse(name)
     root = tree.getroot()
     for element in root.iter('table'):
         wella = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters + string.digits))
         line = wella.sub('', str(element[4].text))

         lines.append(line)
         copy_line_num=line_num
         num = len(line.split())
         if len(hash)==0:
                hash.append(line.split()[0] + ' ' + '1')
                for i in range(0, num-1):
                      flag = 0
                      for j in range(0, len(hash)):
                          if (line.split()[i+1] == hash[j].split()[0]) and (copy_line_num !=line_num):
                              hash[j] = hash[j] + ' ' + str(line_num)
                              flag = 1
                              break
                          elif (line.split()[i+1] == hash[j].split()[0]) and (copy_line_num ==line_num): flag = 1
                      if (flag != 1):
                           hash.append(line.split()[i+1] + ' ' + str(line_num))
                line_num=line_num + 1
         else:
                  for i in range(0, num):
                      copy_line_num2 = line_num - 1
                      flag = 0
                      for j in range(0, len(hash)):
                          if (line.split()[i] == hash[j].split()[0]) and (copy_line_num2 !=line_num) and (copy_line_num ==line_num):
                              hash[j] = hash[j] + ' ' + str(line_num)
                              flag = 1
                              break
                          elif (line.split()[i] == hash[j].split()[0]) and (copy_line_num ==line_num): flag = 1
                      if (flag != 1):
                           hash.append(line.split()[i] + ' ' + str(line_num))
                  line_num=line_num + 1

         for j in range(5,13):
             if (element[j].text == '1'):
                lines_rel.append(line)
                line_num=line_num - 1
                if len(hash_rel)==0:
                    hash_rel.append(line.split()[0] + ' ' + '1')
                    for i in range(0, num-1):
                          flag = 0

                          for j in range(0, len(hash_rel)):
                              if (line.split()[i+1] == hash_rel[j].split()[0]) and (copy_line_num !=line_num):
                                  hash_rel[j] = hash_rel[j] + ' ' + str(line_num)
                                  flag = 1
                                  break
                              elif (line.split()[i+1] == hash_rel[j].split()[0]) and (copy_line_num ==line_num): flag = 1
                          if (flag != 1):
                               hash_rel.append(line.split()[i+1] + ' ' + str(line_num))
                    line_num=line_num + 1
                else:
                            for i in range(0, num):
                                  copy_line_num2 = line_num - 1
                                  flag = 0
                                  for j in range(0, len(hash_rel)):
                                      if (line.split()[i] == hash_rel[j].split()[0]) and (copy_line_num2 !=line_num) and (copy_line_num ==line_num):
                                          hash_rel[j] = hash_rel[j] + ' ' + str(line_num)
                                          flag = 1
                                          break
                                      elif (line.split()[i] == hash_rel[j].split()[0]) and (copy_line_num ==line_num): flag = 1
                                  if (flag != 1):
                                       hash_rel.append(line.split()[i] + ' ' + str(line_num))
                            line_num=line_num + 1
                break
         # if flag2 == 1:
         #     line_num=line_num + 1

ci = dict({})
n = len(lines) # кол-во строк
r = len(lines_rel) # кол-во релевантных строк
c = 0

for i in range(0, len(hash)):
    for j in range(0, len(hash_rel)):
      if (hash[i].split()[0]==hash_rel[j].split()[0]):
        ri = len(hash_rel[j].split())-1
        ai = ri/r
        ni = len(hash[i].split())-1
        bi = (ni - ri)/(n-r)
        ci[hash_rel[j].split()[0]] = math.log2(((ri+0.5)/(r-ri+0.5))/((ni-ri+0.5)/(n-ni-r+ri+0.5)))
        c += (math.log2((1-ai)/(1-bi)))
        break



f = open('result.csv', 'w')
for word in ci:
     f.write(word+';')
     f.write(str(ci[word]))
     f.write('\n')
f.write('\nC;'+str(c)+'\n')
f.close()

phrase = 'Ряд российских олигархов'
phrase = re.split('\.| |,|;', phrase)

result = c
for word in phrase:
     if ci.get(word) is not None:
         result += ci[word]
print(result)
