from assignment3.genre_classification import data_preparation, classification
from data import collect_data, batch_download
from evaluation import similarity
from nlp_spacy import extraction_person
from nrc import emotion_storyline

if __name__ == '__main__':
    # collect_data('meta.json')
    # extraction_person()
    # emotion_storyline()
    # similarity()
    # collect_data('new_meta.json')
    # data_preparation()
    classification('new_result.json')