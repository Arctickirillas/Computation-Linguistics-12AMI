import csv
import nltk
import string
import sys
import argparse


def read_and_preparation(text, word):
    reader = csv.reader(open(text))
    count = 0 
    list_word = []
    dict_text = {}
    dictionary = {}
    for i in reader:
        count+=1
        line = ''.join(i)
        line.replace('.', ' ')
        tokens = nltk.word_tokenize(line)
        tokens = [i for i in tokens if ( i not in string.punctuation )]
        tokens = [i.replace(".", "").lower() for i in tokens]
        dict_text['doc'+str(count)] = tokens
        list_word += tokens
    dict_unique = {}
    list_word = list(set(list_word))
    list_number = []
    for i in range(len(list_word)):
        list_number.append(i+1)
    list_num_and_word = zip(list_word, list_number)
    #print list_num_and_word

    for key, val in dict_text.iteritems():
        list_num = []
        list_w = []
        for i in range(len(list_num_and_word)):
            #print list_num_and_word[i][0],'\t','---->','\t', i+1
            if list_num_and_word[i][0] in val:
               list_num.append(i+1)
               list_w.append(list_num_and_word[i][0])
               num_word = zip(list_num, list_w)
               num_word.reverse()
        dict_unique[key] = num_word
   
    for key1, val1 in dict_text.iteritems():
        num1 = []
        word1 = []
        index_word = []
        for i in range(len(val1)):
            num1.append(i+1)
            word1.append(val1[i])
            index_word = zip(num1, word1)
        dictionary[key1] = index_word

    result_dict = {}    
    for key2, val2 in dict_unique.iteritems():
        for key3,val3 in dictionary.iteritems():
            if key3 == key2:                
                for i in range(len(val2)):
                    result_list = []
                    add_list = []
     #              print v[i][1],'\t-->\t',v[i][0],'\t',i+1,'\t', k
                    result_list.append((val2[i][0]))
                    result_list.append(i+1)
                    result_list.append(key2)
                    if val2[i][1] in result_dict:
                        add_list.append(result_dict[val2[i][1]])
                        add_list.append(result_list)
                        result_dict[val2[i][1]] = add_list
                    else:
                        result_dict[val2[i][1]] = result_list
    find_word(result_dict, word)
    return result_dict
    
def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-n', '--word', nargs='+')
    return parser    
    
    
def find_word(result_dict, word):
    
    f_word = result_dict.get(word)
    print "FIND WORD",'\t', '--->','\t', word
    print "[POSITION, UNIQ_NUMBER, DOCUMENT]",'\t', '--->','\t', f_word
    return f_word
    
if __name__ == "__main__":
    text = '/home/andrew/text.csv'
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    #print (namespace)
    for name in namespace.word:    
        if len (sys.argv) > 1:
            word =  "{}".format(name)
            read_and_preparation(text,word)
        else:
            print "ERROR!\nDo not introduced parameters: file name or word!"