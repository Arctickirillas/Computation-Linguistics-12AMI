import xml.etree.ElementTree as etree

def parse_xml():
    text_data = []
    text_list = []

    tree = etree.parse('/home/andrew/an.xml')
    root = tree.getroot()

    for text in root.iter('sentence'):
        text_data.append([source_tag.text for source_tag in text.iter('source')])
        for tokens_tag in text.iter('tokens'):
            token_tag_list = []
            for token_t in tokens_tag.iter('token'):
                attrb = []
                token_dictionary = {}
                for g_tag in token_t.iter('g'):
                    #print(g.get('v'))
                    attrb.append(g_tag.get('v'))
                token_dictionary[token_t.get('text')] = attrb
                token_tag_list.append(token_dictionary)
            text_list.append(token_tag_list)

    markup_sentence(text_data, text_list)
    return print(text_list, '\n', text_data)

def markup_sentence(text_data, text_list):
    markup_dictionary_words = {}

    for text_i in text_list:
        for word_i in text_i:
            for key,val in word_i.items():
                markup_dictionary_words[key.lower()] = val[0]

    markup_dictionary_sentence = {}
    for text_ii in text_data:
        mark_sheet = []
        for word_ii in text_ii[0].split(' '):
            if word_ii in markup_dictionary_words:
                mark_sheet.append(markup_dictionary_words.get(word_ii))
            else:
                pass
        markup_dictionary_sentence[text_ii[0]] = mark_sheet
    #print(markup_dictionary_sentence)
    return print(markup_dictionary_sentence)

if __name__ == "__main__":
    parse_xml()
