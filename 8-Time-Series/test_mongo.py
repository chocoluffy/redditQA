from __future__ import division
import operator
import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path
import re

con = MongoClient('localhost', 27017)
db = con.test

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
cursor = db.docs_31G.aggregate(pipeline = pipe, allowDiskUse = True)
total_count = len(list(cursor))
print("totoal count...", total_count)
for document in db.docs_31G.aggregate(pipeline = pipe, allowDiskUse = True):
    counter += 1
    if counter < total_count * 0.08: # only use the top 8% most active subreddit data.
        print "Processing #%d subreddit"%(counter)
        docset = " ".join(map(lambda x: x["body"], document['comments']))
        sub_data[document['_id']]['docset'] = docset
        sub_data[document['_id']]['length'] = document['commentsCount']
