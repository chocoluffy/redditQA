# -*- coding: utf-8 -*-

import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path
import urllib
from bs4 import BeautifulSoup
from bson.objectid import ObjectId
import requests
import jieba
import gensim
from gensim import corpora
import os.path
import numpy

stopwords = []
for line in open('stopwords.dat', 'r'):
    word = line.rstrip().decode('utf8') # strip off newline and any other trailing whitespace
    stopwords.append(word)
    
blackword_lst = [
    "约克", 
    "论坛",
    "月",
    "日",
    "超级", 
    "生活",
    "多伦多",
    "吃喝",
    "玩乐",
    "http",
    "ca",
    "征稿",
    "小编",
    "微博",
    "转发理由",
    "编",
    "年"
]

for bad_word in blackword_lst:
    stopwords.append(bad_word.decode('utf8'))

def clean(doc):
    """
    Use chinese stopword and tokenizer to obtain clean doc array. 
    Output, array of string, join by tokens.
    """
    token_lst = jieba.cut(doc, cut_all=True)
    token_lst = filter(lambda x: x not in stopwords, token_lst)
    # print("Full Mode: " + "/ ".join(token_lst))
    return " ".join(token_lst)

if not os.path.exists('models/tokens.dict'):
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5)
    dictionary.save('models/tokens.dict')
else:
    dictionary = corpora.Dictionary.load('models/tokens.dict')
    print("preprocessed dictionary loaded...")


# Save LDA model
if not os.path.exists('models/model.lda'):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(doc_term_matrix, num_topics=15, id2word = dictionary, passes=50)
    ldamodel.save('models/model.lda')
else:
    ldamodel = gensim.models.ldamodel.LdaModel.load('models/model.lda')
    print("lda model loaded...")


def get_topic_from_query(question):
    important_words = clean(question).split(" ")

    dictionary = corpora.Dictionary.load('models/tokens.dict')

    ques_vec = []
    ques_vec = dictionary.doc2bow(important_words)

    topic_vec = []
    topic_vec = ldamodel[ques_vec]

    word_count_array = numpy.empty((len(topic_vec), 2), dtype = numpy.object)
    for i in range(len(topic_vec)):
        word_count_array[i, 0] = topic_vec[i][0]
        word_count_array[i, 1] = topic_vec[i][1]

    idx = numpy.argsort(word_count_array[:, 1])
    idx = idx[::-1]
    word_count_array = word_count_array[idx]

    final = []
    final = ldamodel.print_topic(word_count_array[0, 0], 10)

    question_topic = final.split('*') ## as format is like "probability * topic"

    print "==="
    print question
    print ' '.join(question_topic)
    print "==="

## Evaluation matrix. 
# - original data contains tags.
# - ...


## How to improve model!

test_titles = [ 
{
    "title_short": "我看了一季高达，然后。"
}
]

for obj in test_titles:
    get_topic_from_query(obj["title_short"])