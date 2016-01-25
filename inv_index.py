# -*- coding: utf-8 -*-
"""
@author: Alexey Oskin
"""

def inv_index(file, request):
    
    import re
    
    f = open(file)
    txt = f.read()
    txt_array = txt.split('\n')
    f.close()
    
    request = request.lower()
    request_array = request.split(' ')

    result = []
    
    for string in txt_array:
        mark = False
    
        lstring = string.lower()
        lstring = re.sub(r'[^\w\s]+|[\d]+', r'', lstring).strip()

        word_array = []
        word_array = lstring.split(' ')
        
        for word in request_array:
            try:
                temp = word_array.count(word)
            except:
                temp = 0
            if temp != 0:
                mark = True
            else:
                mark = False
                break
        if mark == True:
            result.append(string)
    
    if len(result) != 0:  
        print ('Search results: \n')
        for a in result:
            print (a, '\n', '----------' )
    else:
        print ('No matches found \n')
    
request = input('Enter your search string: ')
print ()   
inv_index('texts.csv', request)
