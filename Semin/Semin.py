import lxml.html as xml
import time
import pickle
import string
import re


def riaData(fname = 'text_list.csv'):
    page1 = xml.parse('http://ria.ru/lenta/')
    tags = page1.getroot().xpath('//*[@class="list_item_text"]/h3/a')
    base_url = 'http://ria.ru'

    f = open(fname, 'w')
    for tagi in tags:

        try:
            page = xml.parse(base_url + tagi.get('href'))
            root = page.getroot()

            tag = root.xpath('//*[@id="article_full_text"]').pop()
            strit = str(tag.text_content())
            strit = strit.replace('\n', ' ')
            time.sleep(0.1)
            f.write(strit+'\n')
        except:
            time.sleep(1)
    f.close()


#функция составляет индекс и немного изменяет исходный текст, удаляя их него пунктуацию и английские символы
def reindex(fTextName = 'text.csv', fIndexName = 'index_ria_texts.pickle'):

    #считал с файла
    regex = re.compile('[%s]' % re.escape(string.punctuation + string.ascii_letters))
    f = open(fTextName, 'r')
    all = f.read()
    f.close()
    texts = all.split('\n')
    #создаем индекс
    di = dict({})
    index = 0
    for text in texts:
        text = regex.sub(' ', text)
        stri = text.split()
        for word in stri:
            if (di.get(word) == None):
                di[word] = set()
            di[word].add(index)
        index += 1
    f = open(fIndexName, 'wb')
    pickle.dump(di, f)
    f.close()
    print(di)


fInd = 'index_ria_texts.pickle'
fText = 'text.csv'
#riaData(fText)
#reindex(fText, fInd)


f = open(fInd, 'rb')
di = pickle.load(f)
f.close()
print(di)
s = input('Enter the line\n')
s = re.split('\.| |,|;', s)
if(di.get(s[0]) == None ):
    print("Nothing\n")
else:
    result = di[s[0]]
    for word in s:
        result = result.intersection(di[word])

    f = open(fText, 'r')
    texts = f.read()
    texts = texts.split('\n')
    f.close()
    print (result)
    for num in result:
        print(texts[num])

