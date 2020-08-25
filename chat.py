import nltk
nltk.download('wordnet')

import tensorflow as tf
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from tensorflow.python.keras import Sequential
from tensorflow.keras.optimizers import SGD
import random
from tensorflow.python.keras.layers import Dense, Dropout, Activation


words=[]
classes = []
documents = []
ignore_words = ['?', '!','.',',']
data_file = open('intents.json').read()
intents = json.loads(data_file)


for intent in intents['intents']:
    for pattern in intent['utterances']:
        # tokenization
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # adding documents in the corpus
        documents.append((w, intent['tag']))
        # adding to class
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# lemmatization
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))

# documents == combination between patterns and intents
print (len(documents), "documents")

# classes == intents
print (len(classes), "classes", classes)

# words == all words, vocabulary
print (len(words), "unique lemmatized words", words)
pickle.dump(words,open('words.pkl','wb'))
pickle.dump(classes,open('classes.pkl','wb'))

# creating our training data
training = []

# create an empty array for our output
output_empty = [0] * len(classes)

# training set, bag of words for each sentence
for doc in documents:
    # initialize bag of words
    bag = []

    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    print(pattern_words)

    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        print(w)
        bag.append(1) if w in pattern_words else bag.append(0)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)

        print(bag)
        print(doc)
        output_row[classes.index(doc[1])] = 1
        print(output_row)
        training.append([bag, output_row])

# shuffle features and turn into np.array
random.shuffle(training)
training = np.array(training)

# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
# number of neurons equal to number of intents to predict output intent with softmax
model.add(Dense(len(train_y[0]), activation='softmax'))

# SGD == Stochastic gradient descent and Nesterov accelerated gradient
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print("model created")