"""
Train word2vec model on most active subreddits.abs

- pure word2vec.
- word2vec,together with attaching subreddit name after most voted comments.
- sense2vec, use Spacy to POS tag each term, then trian word2vec.

"""
from __future__ import division
import operator
import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path
import re

# Gloabl Configuration
VERSION_PATH = './models/word2vec'
WORDVEC_PATH = os.path.join(VERSION_PATH, 'model')
TF_IDF = True



subreddits = []
data = []
commentCounters = []
# counter = 0

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

# 898 subreddit with >100 ups comments concated, from rc-2015-06 10G data.
def load_from_file():
    with open('3-results-20170921-224241.json') as f:
        for line in f:
            obj = json.loads(line)
            subreddits.append(obj["subreddit"])
            data.append(obj["comments"])
            commentCounters.append(obj["countcomments"])

# use pymongo to load large chunk of data from mongo.
def load_from_mongo():
    if not os.path.exists('./models/4G_top008subreddit_top1kcomments.pkl'):
        # Use pymongo to achieve same effect as below codes. 
        pipe = [
            {'$sort': {"ups": -1 }}, # sort before grouping, so that the comments array is sorted in order.
            {'$group': {'_id': '$subreddit', 'comments': { '$push':  { 'body': "$body", 'ups': "$ups" } }}},
            {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
            { "$project": { 
                "comments": { "$slice": [ "$comments", 1000 ] }, # slice the top 100 comments.
                "commentsCount": 1
            }},
            {"$sort": {"commentsCount": -1}}
        ]

        sub_data = defaultdict(dict)
        counter = 0
        cursor = db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = len(list(cursor))
        print("totoal count...", total_count)
        for document in db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True):
            counter += 1
            if counter < total_count * 0.08: # only use the top 8% most active subreddit data.
                print "Processing #%d subreddit"%(counter)
                docset = " ".join(map(lambda x: x["body"], document['comments']))
                sub_data[document['_id']]['docset'] = docset
                sub_data[document['_id']]['length'] = document['commentsCount']
        print("local comments data saved...")
        pickle.dump(sub_data, open("./models/4G_top008subreddit_top1kcomments.pkl", 'wb'))
        for label, obj in sub_data.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])
    else:
        reddit_comments = pickle.load(open("./models/4G_top008subreddit_top1kcomments.pkl", 'rb'))
        print("local comments data loaded...")
        for label, obj in reddit_comments.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])


load_from_mongo()

# compile documents
doc_complete = data

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
import string
import gensim
from gensim import corpora
from gensim.models import Word2Vec
import os.path

# If dictionary model exists, use it; Otherwise, save a new one.
link_re = re.compile(r'\[([^]]+)\]\(https?://[^\)]+\)')

if not os.path.exists(WORDVEC_PATH):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    def clean(doc):
        """
        - eliminate md,
        - sub special chars,
        - remove stopwords, 
        - punctuation, 
        - links, 
        - numbers, 
        - long words(>20), 
        - and normalize them.
        """
        text = link_re.sub(r'\1', doc)
        text = text.replace('&gt;', '>').replace('&lt;', '<')
        text = re.sub(r"http\S+", "", text) # remove url
        text = " ".join(re.findall('[A-Z][^A-Z]*', text)) # dismantle hashtag style words, such as: OnePieceIsGreat
        text = re.sub(r'\d+', "", text) # remove numbers
        text = " ".join([i for i in text.lower().split() if i not in stop and len(i) > 2 and len(i) < 20]) # remove stopword and longwords.
        text = ''.join(ch for ch in text if ch not in exclude) # remove punctuation
        text = " ".join(lemma.lemmatize(word) for word in text.split()) # stem
        return text

    doc_clean = [clean(doc).split() for doc in doc_complete] 
    model = Word2Vec(doc_clean, size=100, window=5, min_count=5, workers=4)
    model.save(WORDVEC_PATH)
    print("Word2vec model saved...")
else:
    model = Word2Vec.load(WORDVEC_PATH)
    print("Word2Vec model loaded...")
