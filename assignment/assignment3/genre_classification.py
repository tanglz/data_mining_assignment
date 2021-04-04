from nrclex import NRCLex
from functions import load_txt
import json
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier


def data_preparation():
    with open('new_meta.json', 'r') as f:
        json_data = json.load(f)
    for item in json_data:
        title = item['title']
        file_name = 'scripts/' + title + '.txt'
        script_txt = load_txt(file_name)
        if len(script_txt) <= 0:
            continue
        text_object = NRCLex(script_txt)
        raw_emotion_scores = text_object.raw_emotion_scores
        emotions = raw_emotion_scores.items()
        s = sum(raw_emotion_scores.values())
        for key, value in emotions:
            item[key] = value / s
    with open('new_result.json', 'w') as result_file:
        json.dump(json_data, result_file)


def classification(file_name):
    with open(file_name) as data_file:
        json_data = json.load(data_file)
    df = pd.json_normalize(json_data)
    genres = np.array(df[['genres']])
    ge_list = list()
    for gen in genres:
        ge_list.append(gen[0][0])
    col = ['fear', 'joy', 'negative', 'sadness', 'surprise', 'positive', 'trust', 'anticipation', 'anger', 'disgust']
    df = df[col].replace(np.NAN, 0)
    df['genre_1'] = ge_list
    X = df.iloc[:, :-1].values
    Y = df['genre_1'].values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.20)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    classifier = KNeighborsClassifier(n_neighbors=5)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    result = confusion_matrix(y_test, y_pred)
    result1 = classification_report(y_test, y_pred, zero_division=1)
    print("Classification Report:", )
    print(result1)
    result2 = accuracy_score(y_test, y_pred)
    print("Accuracy:", result2)
