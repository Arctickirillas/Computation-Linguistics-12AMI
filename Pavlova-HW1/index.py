__author__ = '315-7'

import lxml.html as html
import time
import pickle


hash = []
f = open('data.csv', 'r')
line_num = 1
lines = []
for line in f:
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
f.close()


words = 'cat father broom'
stroki = []
for i in range(0, len(words.split())):
        length = len(hash)
        for j in range(0, length):
            if words.split()[i] == hash[j].split()[0]:
                for k in range(1, len(hash[j].split())):
                    stroki.append(hash[j].split()[k])
                break
print ('Strings:')
print (stroki)

for i in range(0, len(stroki)):
    for j in range(0, len(lines)):
        if int(stroki[i])-1 == j:
            print (lines[j])
            break