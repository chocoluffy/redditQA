"""
Some tips:
- Make sure use a relatively balanced dataset, each subreddit with 10000 comments. Check the last one's comment count.
- Before training on TF-IDF, need to de-normalize it into normal integer!

Goal:
Finally will save data into each_author_topic_comments.pkl, for further process in author_*.py and subreddit_*.py 

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
VERSION_PATH = './models/no_tfidf_topic_100_8G_data'

DICTIONARY_PATH = os.path.join(VERSION_PATH, 'dictionary.dict')
CORPUS_PATH = os.path.join(VERSION_PATH, 'corpus.mm')
CORPUS_TFIDF_PATH = os.path.join(VERSION_PATH, 'corpus-tfidf.mm')
LDA_PATH = os.path.join(VERSION_PATH, 'model.lda')
TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments_with_author.pkl')
AUTHOR_TOPICS = os.path.join(VERSION_PATH, 'author_topics.pkl')
AUTHOR_STATS_WITH_CONTRIBUTION_COUNT = os.path.join(VERSION_PATH, 'each_author_topic_comments_with_count.pkl')
COMPLETE_AUTHOR_STATS = os.path.join(VERSION_PATH, 'complete_author_stats.pkl') # complete author stats.
SUBREDDIT_CSV = os.path.join(VERSION_PATH, '8G_subreddit.csv')
REDDIT_ALL = os.path.join(VERSION_PATH, 'reddit_all.pkl')


TF_IDF = False
MULTI_CORE = True



# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

# use pymongo to load large chunk of data from mongo.
def load_from_mongo():
    if not os.path.exists(TOP_COMMENTS):
        # Use pymongo to achieve same effect as below codes. 
        pipe = [
            {'$sort': {"ups": -1 }}, # sort before grouping, so that the comments array is sorted in order.
            {'$group': {'_id': '$subreddit', 'comments': { '$push':  { 'ups': "$ups", "author": "$author" } }}},
            {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
            { "$project": { 
                "comments": { "$slice": [ "$comments", 2500 ] }, # slice the top comments.
                "commentsCount": 1
            }},
            {"$sort": {"commentsCount": -1}},
            {"$out" : "top_comments" }
        ]

        sub_data = defaultdict(dict)
        counter = 0
        cursor = db.docs_l8.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = db.top_comments.find({}).count()
        print("totoal count...", total_count)
        for document in db.top_comments.find({}):
            counter += 1
            if counter < total_count * 0.33: # only use the top most active subreddit data.
                print "Processing #%d subreddit"%(counter)
                sub_data[document['_id']]['top_comments'] = document['comments']
                sub_data[document['_id']]['length'] = document['commentsCount']
        print("local comments data saved...")
        pickle.dump(sub_data, open(TOP_COMMENTS, 'wb'))
    else:
        reddit_comments = pickle.load(open(TOP_COMMENTS, 'rb'))
        print("local comments data loaded...")


load_from_mongo()
