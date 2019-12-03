import pandas as pd
import numpy as np
import os
import re
import spacy
import gensim
from gensim.models.phrases import Phrases, Phraser
from time import time 
import multiprocessing
from gensim.models import Word2Vec

from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split


import tensorflow as tf
import tensorflow_hub as hub

import keras 
from keras.models import Sequential, Model 
from keras import layers
from keras.wrappers.scikit_learn import KerasClassifier
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, Input, Embedding
from keras.layers.merge import Concatenate
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle
from sklearn.metrics import confusion_matrix, f1_score, accuracy_score, mean_squared_error



# loading synthesised intents data
data = pd.read_csv('data_intents.csv')

# dummy variable for labels
label = pd.get_dummies(data['intent'])
data = pd.concat([data,label],axis=1)

# features and label
x = data['sentences']
y = data[['API calls', 'about_chatbot', 'annoyed', 'applause',
        'get_instructions',	'get_recipe', 'goodbye', 'gratitude', 'greet']]




# universal encoder word embeddings
g = tf.Graph()
with g.as_default():
    text_input = tf.placeholder(dtype=tf.string, shape=[None])
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
    embedded_text = embed(text_input)
    init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
    g.finalize()

# session created and initialized.
session = tf.Session(graph=g)
session.run(init_op)

def word_embeddings(input_text):
    emb = session.run(embedded_text, feed_dict={text_input: input_text})
    return emb


# word embeddings
emb_x = word_embeddings(x.astype(str))

# train-test split
x_train, x_test, y_train, y_test = train_test_split(emb_x,y,random_state=1)


# nn_classifier
def model():
    model = Sequential()

    model.add(Dense(128, activation='relu', kernel_initializer='random_normal',input_dim=512))# input
    model.add(Dense(9, activation='softmax', kernel_initializer='random_normal')) # target shape
    model.compile(optimizer='adam',
                loss='categorical_crossentropy',
                metrics=['accuracy'])
    model.summary()
    return model


model = model()
model.fit(x_train, y_train,
            epochs=20,
            batch_size=250,verbose=1)
                                # validation_data=(x_val, y_val))

y_pred = model.predict(x_test)


# evaluate model
train_acc = model.evaluate(x_train,y_train)
test_acc = model.evaluate(x_test, y_test)

# confusiion matrix
# confusion_matrix(y_test,y_pred)


# index2Intent
labels = data['intent'].values
ids = data['Label'].values
idx2intent = {i:j for i, j in zip(ids, labels)}
intent idx2intent[0]

# get intent
def get_intent(pred):

    result = np.amax(pred)
    index = np.where(pred == np.amax(pred))
    index = list(index[1])
    intent = idx2intent[index[0]]

    return intent

# test_case
text = 'suggest me some recipe'
text = word_embeddings([text])
pred = model.predict(text)

get_intent(pred)

# saving trained model
pickle.dump(model, open("../models/Intent_Model/intent_classification_model_v05.pkl", "wb" ) )