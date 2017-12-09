"""
Given author stats on its contributions. 

Aggregate, only need its contribution count, not votes. For top 80% authors.
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

VERSION_PATH = './models/201301'
AUTHOR_STATS_WITH_CONTRIBUTION_COUNT = os.path.join(VERSION_PATH, 'author_comments_stats.pkl')


pipe = [
    {'$sort': {'ups': -1}},
    {'$group': {
        '_id': '$author',
        'contributions': { '$push':  { 'subreddit': "$subreddit", 'ups': "$ups" } },
        'subredditset': {'$addToSet': "$subreddit"}
    }},
    {'$addFields': { 'subredditnum': { '$size': "$subredditset" } } },
    {'$addFields': { 'commentsCount': { '$size': "$contributions" } } },
    { "$project": { 
        "subredditset": 0
    }},
    {'$match': {
        '$and': [ 
            {'subredditnum': {'$gt': 5}},
            {'commentsCount': {'$lt': 300}} # at least 10 comments per day.
        ]}
    },
    {"$sort": {"commentsCount": -1}}
]

author_dict = defaultdict(dict)
for document in db.docs_201301.aggregate(pipeline = pipe, allowDiskUse = True): # change different db name here.
    author_name = document['_id']
    contributions = defaultdict(int)
    contributions_by_count = defaultdict(int)
    for comment_info in document['contributions']:
        contributions[comment_info['subreddit']] += comment_info['ups']
        contributions_by_count[comment_info['subreddit']] += 1
    author_stats[author_name]['contributions'] = contributions
    author_stats[author_name]['contributions_by_count'] = contributions_by_count
    author_stats[author_name]['subreddit_num'] = document['subredditnum']
    author_stats[author_name]['comments_count'] = document['commentsCount']


pickle.dump(author_stats, open(AUTHOR_STATS_WITH_CONTRIBUTION_COUNT, 'wb'))
print("saved stats for each user...")