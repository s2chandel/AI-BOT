
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
import tensorflow_hub as hub
import operator
import pickle
import re
import random
from newsapi import NewsApiClient
from check_name import check_name
from find_news import find_news
import pymssql
pymssql.__version__
'1.0.3'
# mysql conn


# Data
data = pd.read_sql_query('''SELECT* FROM [dbo].[Faq.QuestionAnswer]''', conn)

# tfidf
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3))
ques_vectors = tfidf.fit_transform(data['question'])



def find_FAQ_score(answer):
    selected_qna_vector = tfidf.transform([answer])
    cosine_similarities = cosine_similarity(selected_qna_vector, ques_vectors)
    (index,value) = max(enumerate(list(cosine_similarities[0])), key=operator.itemgetter(1))
    return (index,value)


def final_answer(text):
    (index, value) = find_FAQ_score(text)
    if value <= 0.2:
        message = "Sorry I don't have a response to your question"
        return message
    else:
        print("----Question asked by the user----")
        ques = data['question'].values
        ans = data['answer'].values
        (index, value) = find_FAQ_score(text) 
        print(ques[index])
        final_answer = ans[index]
        clean = re.compile('<.*?>')
        final_answer = re.sub(clean,' ', final_answer)
        print("----Response----")
        return final_answer


class DialogueManager:

  def __init__(self):

    #LOAD MODELS
    self.IntentModel = pickle.load(open("models/Intent_Model/intent_classification_model.pkl", "rb"))
    self.idx2intent = pickle.load(open("models/Intent_Model/idx2intent.pkl", "rb"))
    self.TFsession, self.embedded_text, self.text_input = self.initializeTfSession()


  def initializeTfSession(self):
    # Create graph and finalize.
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
    return (session, embedded_text, text_input)

  def reset(self, chat):
    chat['intent'] = ""
    chat['last_intents']=["",""]
    return chat

  def get_intent(self, text):
    new_text = [text.lower()]
    new_text = self.TFsession.run(self.embedded_text, feed_dict={self.text_input: new_text})
    y_pred = self.IntentModel.predict(new_text)
    pred_prob = self.IntentModel.predict_proba(new_text)                                #pairwise probabilities for each class
    max_prob = np.amax(pred_prob)                                                       #max_prob:max prob among the quantified classifiers 
    print("max prob---")
    print(max_prob)
    
    if (max_prob>=0.40) or (text.lower()=="yes") or (text.lower()=="no"):                 #threshold if the max arg is less than 0.4
      return self.idx2intent[y_pred[0]]
    else:
      return ""



  def NLU(self, text, chat):
    print("chat-->")
    print(chat)
    print(text)
    intent = self.get_intent(text)

    # GROUNDING based on context
    print(chat['last_intents'][-1])
    if intent == "" and chat['last_intents'][-1] == 'API calls':
      intent="API calls"

    elif intent =="": 
      message = "Sorry I don't have a resonse for that."
      return message, chat

    print("Intent found: {}".format(intent))

    nlu = {"intent": intent}
    chat['intent'] = intent
    chat['last_intents'].append(intent)
    message, chat = self.finite_state_machine(nlu, chat, text)
    return message, chat

  def finite_state_machine(self, nlu, chat, text):
    if nlu['intent'] == "greet":
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      first_name = check_name(chat['user_id'])
      greets = ["Hi! "+first_name+"" ,"I’m good "+first_name+"", "how are you?", "I am fine, what about you?", 'All good, thanks!']
      greets_short =["Hi "+first_name+"", "Hi there", "Hello! "+first_name+"","Heya", "Hello! there"]
      if len(text.split())<=2:
        message = random.choice(greets_short)
      else:
        message = random.choice(greets)+"\nWhat can I do for you?"    
      return message, chat

    if nlu['intent']== 'applause':
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      first_name = check_name(chat['user_id'])
      applause = ["I’m glad you think so", "I just try", "Thanks "+first_name+""]
      message = random.choice(applause)
      return message, chat
    
    if nlu['intent']== 'annoyed':
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      first_name = check_name(chat['user_id'])
      message = "Are you unsatisfied with my service?\n Yes/No"
      if (nlu['intent'] =='annoyed'and text.lower() == 'yes'):
        annoyed = ["Sorry! I’m still learning","Sorry! If I wasn’t up to your expectations", "I’m trying to improve"]
        message = random.choice(annoyed)
      if (nlu['intent']=='annoyed'and text.lower() == 'no'):
        message = "Great! How can I help you "+first_name+"?"
      return message, chat


    if nlu['intent']== 'about_chatbot':
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      introduction=["Hello! I’m your virtual AI assistant developed at Diabetes Digital Media","I am an AI Bot designed at Diabetes Digital Media"]
      message = random.choice(introduction)
      return message,chat
      
    if nlu['intent'] == "faq":
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      (index, value) = find_FAQ_score(text)
      if value <= .35:
        message = "Sorry I dont have a response for that.\n This is what I found on google:\n"
        print(message)
        message+= search_google(text)
        return message, chat
        # message = "This is what I found on wikipedia:\n"
        # print(message)
        # message+= search_wikipedia(text)
        # return message, chat
      else:
        message = final_answer(text)
        return message, chat

    if nlu['intent'] == "API calls":
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)

      if chat['last_intents'][-2] == "API calls":
        message = find_news(text)
        message = str(message)
        chat = self.reset(chat)
      else:
        message = "What's your topic of interest?"

      return message,chat

    if nlu['intent'] == "goodbye":
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      goodbye = ["Bye!","Okay! Talk to you later", "Bye! Bye!", "Later then"]
      message = random.choice(goodbye)
      return message, chat

    if nlu['intent'] == "gratitude":
      if chat['last_intents'][-2] in ["get_recipe", "get_instructions"]:
        chat = self.reset(chat)
      gratitude = ["No Problem!","Glad that you like my service", "No worries", "Anytime here to help you"]
      message = random.choice(gratitude)
      return message, chat


GrowBot_objects = {}
dm = DialogueManager()

class GrowBot:

    def __init__(self, user_id):
        self.chat = {}
        self.chat['user_id'] = user_id
        # self.chat['category_ids'] = []
        # self.chat['dietary_type_ids'] = []
        # self.chat['cuisine_id'] = None
        # self.chat['number_of_recipes'] = 0
        self.chat['intent'] = ""
        # self.chat['entities'] = []
        # self.chat['selected_entities'] = {"category": 0, "cuisine": 0, "dietarytype": 0}
        self.chat['last_intents'] = ["",""]
        # self.chat['recipe_mapping'] = {}

    def get_response(self, message, chat):
        response = {"message": message, "chat": chat}
        return response

    def reply(self, user_message):
        message, chat = dm.NLU(user_message, self.chat)
        self.chat = chat
        return self.get_response(message, self.chat)

# def save_chat(user_id, message, response):

#     time = datetime.datetime.now()
#     filename = str(user_id)
#     user_message = str(time)+" USER: "+message+"\n"
#     bot_reply = str(time)+" BOT: "+response+"\n"
#     text = user_message+bot_reply

#     if os.path.exists('chats/{}.txt'.format(filename)):
#         mode = "a"
#     else:
#         mode = "w"

#     with open('chats/{}.txt'.format(filename), mode) as myfile:
#         myfile.write(text)

import flask
from io import StringIO    
import json
from flask import Flask
    
def get_GrowBot_response(json):
    if json['user_id'] not in GrowBot_objects.keys():
        bot = GrowBot(json['user_id'])
        GrowBot_objects[json['user_id']] = bot
    else:
        bot = GrowBot_objects[json['user_id']]

    response = bot.reply(json['user_message'])
    # save_chat(json['user_id'], json['user_message'], response["message"])
    return response

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
# api endpoint "/talk"
# Request Body{"user_id":, "user_message":"", "update_id":}
#method="POST" to post resquest from the client side
@app.route('/talk', methods=['POST'])
def MLbot():

   if flask.request.content_type == 'application/json':
       input_json = flask.request.get_json()
       print("Input json")
       print(input_json)
   else:
       return flask.Response(response='Content type should be application/json', status=415, mimetype='application/json')

   # Get the response
   response = get_GrowBot_response(input_json)

   out = StringIO()
   json.dump(response, out)
   return flask.Response(response=out.getvalue(), status=200, mimetype='application/json')



if __name__ == '__main__':
   app.run(port=5000)






