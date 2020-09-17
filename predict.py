import random
import json
from tensorflow.python.keras.models import load_model
import numpy as np
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import re

lemmatizer = WordNetLemmatizer()

model = load_model('models/chatbot_model.h5')

intents = json.loads(open('datasets/intents.json').read())
alternateMeds = json.loads(open('datasets/sample.json').read())
drugDetails = json.loads(open('datasets/drugs.json').read())
words = pickle.load(open('datasets/words.pkl', 'rb'))
classes = pickle.load(open('datasets/classes.pkl', 'rb'))
finddoc = json.loads(open('datasets/doctors.json').read())


def clean_up_sentence(sentence):
    # spell check
    words=[]
    for s in sentence.split():
        words.append(TextBlob(s).correct())

    sentence=' '.join(map(str, words))

    # tokenization
    sentence_words = nltk.word_tokenize(sentence)
    # stemming
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence


def bow(sentence, words, show_details=True):
    # tokenization
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)

    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:

                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]

    # for r in res:
    #     print((float(r)))

    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    # print('after error ----------------->')

    # for r in res:
    #     print((float(r)))

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)

    # print('after sort ----------------->')
    # print((results[0]))
    # for r in res:
    #     print((float(r)))

    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})

    # print('returnlist ----------------->')
    # for r in return_list:
    #     print(r)

    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['answers'])
            break
    return result


def chatbot_response(text):
    ints = predict_class(text, model)
    res = getResponse(ints, intents)
    return res, ints[0]['intent']


def findAlternate(name):
    name = name.capitalize()
    print(name)
    flag = False
    for m in alternateMeds:
        drugs = m['drugs']

        if name in drugs:
            flag = True
            drugs_to_send=drugs
            drugs_to_send.remove(name)
            return drugs_to_send

    if flag != True:
        return ['No alternatives found in database']

def findDoctor(city,specialization):
    city = city.capitalize()
    print(city)
    flag = False
    for m in finddoc:
        doccity = m['city']
        if doccity==city:
            docSpec=m['specialization']
            if docSpec==specialization:
                doctors=m['docs']
                flag=True
                return doctors

    if flag != True:
        return ['No doctors with required expertise in given area']


print(findAlternate("Mylanta"))
print(chatbot_response("i neeed amblnce"))
