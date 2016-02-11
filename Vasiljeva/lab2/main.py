import lxml.etree as et
import math

def make_inv_index(dictionary, str, ind):
    words = str.split()
    for word in words:
        if dictionary.get(word) == None:
            dictionary[word]= set()
            dictionary[word].add(ind)
        else:
            dictionary[word].add(ind)
    return dictionary

relevant_d = dict()
all_d = dict()
for i in range(1,51):
    bank = 'banks/bank (' + str(i) + ').xml'
    f = et.parse(bank)
    root = f.getroot()
    db = root[-1]
    for bank in db[1:]:
        for j in range(5,12):
            if(bank[j].text == '1'):
                twit = bank[4].text
                twitid = bank[0].text
                print(i, j, twit)
                make_inv_index(relevant_d,twit,twitid)
                make_inv_index(all_d,twit,twitid)
                break
            if(bank[j].text == '-1'):
                twit = bank[4].text
                twitid = bank[0].text
                make_inv_index(all_d,twit,twitid)
                break

c_i = dict()
relevant_n = len(relevant_d)
all_n = len(all_d)
C = 0
for word in all_d:
    if (relevant_d.get(word) != None) :
        relevant_n_i = len(relevant_d[word])
        a = relevant_n_i/relevant_n
        all_n_i = len(all_d[word])
        b = (all_n_i - relevant_n_i)/(all_n - relevant_n)
        c_i[word] = math.log(((relevant_n_i+0.5) / (relevant_n-relevant_n_i+0.5)) / ((all_n_i-relevant_n_i+0.5) / (all_n-all_n_i-relevant_n+relevant_n_i+0.5)))
        C += (math.log((1 - a) / (1 - b)))

result_file = open('result.csv', 'w')
for word in c_i:
    result_file.write(word + ';')
    result_file.write(str(c_i[word]))
    result_file.write('\n')
result_file.write('\n C;' + str(C) + '\n')

input_phrase = 'Кипр Райффайзен банк кредит'
input_phrase = input_phrase.split()

result = C
for word in input_phrase:
    if (c_i.get(word) != None):
        result += c_i[word]
print('Релевантность = ', result)


