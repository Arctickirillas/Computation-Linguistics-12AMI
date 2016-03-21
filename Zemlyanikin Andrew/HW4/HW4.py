import pickle
import numpy as np
import os


def get_3gram(location_file_three_grams):
    file = open(location_file_three_grams, 'r')
    text = []
    text_1 = []
    for line in file.readlines():
        text.append(line.replace(',', '').split('\n'))
    for word in text:
        text_1.append(word[0])
    maximum = int(text_1[0].split('\t')[0])
    three_gram_dict = {}
    for word in text_1:
        word_1 = list(filter(None, word.split('\t')))
        three_gram_dict[(word_1[1], word_1[2], word_1[3])] = int(word_1[0]) / maximum
    pickle_path = '/home/andrew/three_gram_dump.pickle'
    if os.path.isfile(pickle_path) == False:
        three_gram_dump = open('/home/andrew/three_gram_dump.pickle', 'ab')
        pickle.dump(three_gram_dict, three_gram_dump)
        three_gram_dump.close()
    else:
        return three_gram_dict


def perplexity_text_data(location_file_text_data):
    summ = 0
    with open('/home/andrew/three_gram_dump.pickle', 'rb') as f:
        gram_dict = pickle.load(f)
    text_data = open(location_file_text_data, 'r')
    for text_i in text_data:
        word_i = text_i.lower().rstrip().lstrip().split()
        if len(word_i) > 2:
            for i in range(len(word_i) - 2):
                if (word_i[i], word_i[i + 1], word_i[i + 2]) in gram_dict:
                    perp = gram_dict[word_i[i], word_i[i + 1], word_i[i + 2]]
                    summ += perp * (np.log(perp))
    perplexity = 2 ** (-1 * summ)
    return print('Perplexity:', perplexity)


if __name__ == "__main__":
    while 1:
        try:
            location_file_three_grams = input('Please, enter the address of the three_grams file:')
            location_file_text_data = input('Please, enter the path of the text data file:')
            get_3gram(location_file_three_grams)
            perplexity_text_data(location_file_text_data)
        except:
            print('Sorry!\n')
