import json

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

from functions import load_txt, first_letter_uppercase, exclusive_word_list

nlp = en_core_web_sm.load()


def extraction_person():
    with open('meta.json', 'r') as json_file:
        data = json.load(json_file)
    for item in data:
        title = item['title']
        file_name = 'scripts/' + title + '.txt'
        script_txt = load_txt(file_name)
        if len(script_txt) <= 0:
            continue
        doc = nlp(script_txt)
        tags = [(X.text, X.label_) for X in doc.ents]
        word_list = []
        for tag in tags:
            if tag[1] == 'PERSON':
                nnp_word = first_letter_uppercase(tag[0])
                word_list.append(nnp_word)
        word_list_reduce = Counter(word_list).most_common(100)
        characters = []
        i=0
        for word_dict in word_list_reduce:
            if i>= 5:
                break
            if word_dict[1] >= 5 and '\x00' not in word_dict[0] and word_dict[0] != 'V.o.':
                characters.append(word_dict[0])
                i =i+1
        item['predict_characters'] = characters
        print(characters)
    with open('result.json', 'w') as output:
        json.dump(data, output)
    return data
