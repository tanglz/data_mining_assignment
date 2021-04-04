# https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm
# https://pypi.org/project/NRCLex/
import json

from nrclex import NRCLex

from functions import load_txt


def emotion_storyline():
    script_txt = "The true story of a young teacher who fights against the board of education in her bid to teach underprivileged kids in a Harlem school the beauty of music through the violin. In her struggle she loses everything as the system comes down on her with all their might but her determination for the kids happiness helps her to battle back with wonderfully inspirational results."
    text_object = NRCLex(script_txt)
    print(text_object.raw_emotion_scores)
    print(text_object.top_emotions)
    return


def emotion_scripts():
    # with open('test.json', 'r') as json_file:
    #     data = json.load(json_file)
    # for item in data:
    #     title = item['title']
    #     file_name = 'scripts/' + title + '.txt'
    #     script_txt = load_txt(file_name)
    # text_object = NRCLex(script_txt)
    # emotion_map = text_object.raw_emotion_scores
    return
