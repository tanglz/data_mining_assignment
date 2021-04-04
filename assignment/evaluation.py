import difflib
import json
import textdistance
from fuzzy_match import match
from fuzzy_match import algorithims


def get_data():
    with open('result.json', 'r') as f:
        data_json = json.load(f)
    return data_json


# if I regard a character name as a class, each movie has different classes
# idea: calculate each movie's accuracy, precise, and recall. Then calculate average.
# each movie has multiple classes (each character name is a class)
# the issue is character name has different patterns, such as first name, last name, both, name with age.
# So, I will regard this as the same class for training data and predicted data.


def similarity():
    with open('result.json', 'r') as f:
        data = json.load(f)
    sm_list = list()
    for item in data:
        origin = item.get('character_name_list')
        prediction = item.get('predict_characters')
        if prediction is None or origin is None:
            continue
        scores = list()
        for n2 in prediction:
            s_c = list()
            for n1 in origin:
                s_c.append(algorithims.trigram(n2, n1))
            scores.append(max(s_c))
        if len(scores) == 0:
            avg = 0
        else:
            avg = sum(scores) / len(scores)
        sm_list.append(avg)
    acc = sum(sm_list) / len(sm_list)

    print("accuracy:"+str(acc))
