import os
import xml.etree.ElementTree as ET
import re
from math import log
import argparse
import sys

def func(path1):
    marks = []
    tws = []
    dir_name = path1
    listdir = os.listdir(dir_name)

    for fname in listdir:
        tree = ET.parse(dir_name+'/'+fname)
        root = tree.getroot()
        banks = root[1]
        twit_class(banks,marks,tws)
    create_data(marks, tws)

def twit_class(banks, marks, tws):

    for bank in banks:
        for i in range(5, 13):
            if bank[i].text == '-1':
                car_mark = 0
                p = bank[4].text
                car_mark = car_mark + 1
                tex(tws,p)
                marks.append(car_mark)
            if bank[i].text == '1':
                car_mark = 0
                p = bank[4].text
                car_mark = car_mark - 1
                marks.append(car_mark)
                tex(tws,p)
    return(tws, marks)

def tex(tws, p):
    tmp_text = re.sub(r'\@\w+', '', p)
    tmp_text = re.sub(r'\#\w+', '', tmp_text)
    tmp_text = re.sub(r'http://[^ ]*', '', tmp_text)
    tmp_text = re.sub(r'https://[^ ]*', '', tmp_text)
    regexp = re.compile('\#'+u'[А-Яа-я]+')
    tmp_text = re.sub(regexp, '', tmp_text)

    regexp = re.compile('\n')
    tmp_text = re.sub(regexp, '', tmp_text)

    regexp = re.compile('\d+')
    tmp_text = re.sub(regexp, '', tmp_text)

    regexp = re.compile(':|!+|(\.)+|\"+|\||\(|\)|%|;|@|/|\$|,|-|\?|[a-zA-Z0-9]|&|«|»|№|~|—|“|…|€|#|')
    tmp_text = re.sub(regexp, '', tmp_text)

    regexp = re.compile('^\s+')
    tmp_text = re.sub(regexp, '', tmp_text)
    tmp_text = str(tmp_text).lower().split(' ')
    result = list(filter(None, tmp_text))
    tws.append(result)

    return (tws)

def create_data(marks, tws):
    valid_list = []
    gen_list = []
    unique_list = []
    info_dict = {}
    for i in range(len(tws)):
        for j in range(len(tws[i])):
            gen_list.append(tws[i][j])
    unique_list = list(set(gen_list))
    valid_list = list(zip(marks, tws))
    R = marks.count(1)
    N_doc = len(valid_list)
    for i in range(len(unique_list)):
        r_i = 1
        n_i = 1
        for j in range(len(valid_list)):
            if unique_list[i] in valid_list[j][1]:
                if valid_list[j][0] == 1:
                    r_i = r_i + valid_list[j][1].count(unique_list[i])
                else:
                    n_i = n_i + valid_list[j][1].count(unique_list[i])
        info_dict[unique_list[i]] = (r_i, R, n_i, N_doc)
    c_i_sol(info_dict)


def c_i_sol(info_dict):
    i = 0
    dict_ci = {}
    for k, v in info_dict.items():
        i+=1
        coeff = float(0.5)
        a_i = round(v[0]/v[1], 3)
        b_i = round((v[2] - v[0])/(v[1] - v[3]), 3)
        c_i = ((a_i + coeff)*(1 - b_i + coeff))/((b_i + coeff)*(1 - a_i + coeff))
        if c_i > 0:
            dict_ci[k] = log(c_i)
    C = 0
    for val in dict_ci.values():
        if val > 0:
            C = C + val
    C_r = log(C)
    print('RESULTS BIRM:\n')
    print('C = ', C_r)

    f = open('/home/andrew/res.csv', 'ab')
    for w, ke in dict_ci.items():
        f.write(bytes(str(w) + ';' + str(ke)+'\n', encoding='cp1251'))
    f.write(bytes(str("C")+';'+str(C_r)+'\n', encoding='cp1251'))

    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    for name in namespace.word:
        if len (sys.argv) > 1:
            word = "{}".format(name)
            g_func(dict_ci, C_r, word)
        else:
            print ("ERROR!\nDo not introduced parameters: file name or word!")

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', '--word', nargs='+')
    return parser



def g_func(dict_ci, C_r, word):
    req_list = word.split(' ')
    g = 0
    for i in range(len(req_list)):
        a = (dict_ci.get(req_list[i], 0))
        print('\n', 'c_i = ',a, '--->', req_list[i])
        if a != 0:
            g = g + a
        else:
            g = g + a*(-1)
    g = g + C_r
    if g > C_r:
        print('\n','relevant, g = ',  g, '>', 'C = ', C_r,'---->', word)
    else:
        print('not relevant, g = ', g, '<', 'C = ',C_r,'---->', word, '\n')

if __name__ == "__main__":
    path1 = '/home/andrew/banks/'
    func(path1)




