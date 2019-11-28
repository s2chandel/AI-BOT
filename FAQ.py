import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
import re
from search_google import search_google

data = pd.read_csv("Data/FAQs.csv")
del data['video_url']
data = data.replace(regex=[r'<p>', '</p>'], value='')

tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 5))
ques_vectors = tfidf.fit_transform(data['question'])

data = data.reset_index()

ques = data['question'].values
ans = data['answer'].values


def find_FAQ_score(answer):
    selected_qna_vector = tfidf.transform([answer])
    cosine_similarities = cosine_similarity(selected_qna_vector, ques_vectors)
    (index,value) = max(enumerate(list(cosine_similarities[0])), key=operator.itemgetter(1))
    return (index,value)
    
def final_answer(user_message):
    (index, value) = find_FAQ_score(user_message)
    print("----Question asked by the user----")
    ques = data['question'].values
    ans = data['answer'].values
    (index, value) = find_FAQ_score(user_message) 
    print(ques[index])
    final_answer = ans[index]
    clean = re.compile('<.*?>')
    final_answer = re.sub(clean,' ', final_answer)
    print("----Response----")
    return final_answer
###########################

# def find_score(answer):
#     ques = data['question'].values
#     ans = data['answer'].values
#     (index,value) = fuzz.ratio(answer, ques)
#     return (index,value)

# def final_answer(user_message):
#     (index, value) = find_score(user_message)
#     print("----Question asked by the user----")
#     ques = data['question'].values
#     ans = data['answer'].values
#     (index, value) = find_score(user_message) 
#     print(ques[index])
#     final_answer = ans[index]
#     clean = re.compile('<.*?>')
#     final_answer = re.sub(clean,' ', final_answer)
#     print("----Response----")
#     return final_answer

# user_message = "how can i check edit notification settings"
# final_answer(user_message)