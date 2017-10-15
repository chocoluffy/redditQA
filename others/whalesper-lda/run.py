# -*- coding: utf-8 -*-

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


example_url = "http://mp.weixin.qq.com/s?__biz=MzA4NjIyMTUxMQ%3D%3D&mid=2649730605&idx=2&sn=18e6c751f7872b9b170d6ccc4005008d#wechat_redirect"
malform_url = "http://mp.weixin.qq.com/s?__biz=MA4NjIyMTUxMQ%3D%3D&mid=2649730605&idx=2&sn=18e6c751f7872b9b170d6ccc4005008d#wechat_redirect"
mercury_url = "https://mercury.postlight.com/parser"


def extract_wechat_text(link):
    url = link
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    lst = soup.select('#js_content')
    if len(lst):
        text = soup.select('#js_content')[0].get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
    else:
        return ''

def extract_mercury_wechat(link):
    payload = {"url": link}
    r = requests.get(mercury_url, headers={"Content-Type":"application/json", "x-api-key": "BT0V6DwAqKGhdCsxr33PnDkfKNmYLLGouYI4sq3o"}, params=payload)
    return r.json()

# print extract_mercury_wechat(malform_url)

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

def update_mongo_mercury():
    counter = 0
    for document in db.feeds.find({}):
        if document['source'] == 'wechat' and 'html' not in document.keys():
            if counter % 10 == 0:
                print counter
            res = extract_mercury_wechat(document['url'])
            if 'title' in res.keys() and res['title']:
                document['html'] = res['content']
                db.feeds.save(document)
                counter += 1

def update_mongo_fulltext():
    counter = 0
    for document in db.feeds.find({}):
        """
        Update existing documents:
            - wechat, add body field to be fulltext. remove documents of malform links.
            - weibo, use title as body.
        """
        if 'source' in document.keys() and 'body' not in document.keys():
            if counter % 10 == 0:
                print counter
            if document['source'] == 'wechat':
                body = extract_wechat_text(document['url'])
                if body:
                    document['body'] = body
                    db.feeds.save(document)
                else:
                    db.feeds.delete_one({'_id': ObjectId(document['_id'])})
            elif document['source'] == 'weibo':
                document['body'] = document['title']
                db.feeds.save(document)
            else:
                db.feeds.delete_one({'_id': ObjectId(document['_id'])})
            counter += 1
        else:
            if 'source' not in document.keys():
                db.feeds.delete_one({'_id': ObjectId(document['_id'])})
            
def save_data():
    res = []
    for document in db.feeds.find({}, {"weight": 0, "clicks": 0, "col_name": 0, "topic_name": 0, "post_img": 0, "likes": 0, "url": 0}):
        res.append(document)
    pickle.dump(res, open("whalesper.pkl", 'wb'))

def load_data():
    data = pickle.load(open("whalesper.pkl", "rb"))
    # print data[0]
    return data


rawdata = load_data()

import jieba
import gensim
from gensim import corpora
import os.path

stopwords = []
for line in open('stopwords.dat', 'r'):
    word = line.rstrip().decode('utf8') # strip off newline and any other trailing whitespace
    stopwords.append(word)
    


def clean(doc):
    """
    Use chinese stopword and tokenizer to obtain clean doc array. 
    Output, array of string, join by tokens.
    """
    token_lst = jieba.cut(doc, cut_all=True)
    token_lst = filter(lambda x: x not in stopwords, token_lst)
    # print("Full Mode: " + "/ ".join(token_lst))
    return " ".join(token_lst)

# doc_clean = [clean(doc["body"]).split() for doc in rawdata]

if not os.path.exists('models/tokens.dict'):
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5)
    dictionary.save('models/tokens.dict')
else:
    dictionary = corpora.Dictionary.load('models/tokens.dict')
    print("preprocessed dictionary loaded...")

if not os.path.exists('models/doc-term.mm'):
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above. [Bag Of Word]
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Save the matrix into Market Matrix format. 
    corpora.MmCorpus.serialize('models/doc-term.mm', doc_term_matrix)
else:
    doc_term_matrix = corpora.MmCorpus('models/doc-term.mm')
    print("document to term matrix loaded...")

pprint(map(lambda x: (dictionary[x[0]], x[1]), doc_term_matrix[0]))


# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# # Save LDA model
# if not os.path.exists('models/model.lda'):
#     # Creating the object for LDA model using gensim library
#     Lda = gensim.models.ldamodel.LdaModel
#     # Running and Trainign LDA model on the document term matrix.
#     ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
#     ldamodel.save('models/model.lda')
# else:
#     ldamodel = gensim.models.ldamodel.LdaModel.load('models/model.lda')
#     print("lda model loaded...")


# def print_general_subreddit_topic():
#     """
#     Randomly print out 20 topics for human inspection.
#     """
#     ldamodel.print_topics(20)

# print_general_subreddit_topic()


# # clean(rawdata[0]["body"])

# # save_data()
# # update_mongo_mercury()