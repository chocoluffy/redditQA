"""
Given subreddit stats on its contributions. 

- pickle files from ./models/subreddit_vector_201x are trained from year's data.

- procedure:
    - Aggregate by author, only need its contribution count, not votes. For top authors(more complete, the better).
    - calculate G/S score for each author by subreddit embeddings from LSI.
    - Aggregate by subreddit, use involvement, then calculate the G/S score for each subreddit. 
    - Make plot.
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
import itertools
from scipy.interpolate import interp1d
import math
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

VERSION_PATH = './models/201401'
AUTHOR_STATS_WITH_CONTRIBUTION_COUNT = os.path.join(VERSION_PATH, 'author_comments_stats_with_score.pkl')
SUBREDDIT_STATS = os.path.join(VERSION_PATH, 'reddit_stats.pkl')
author_stats = pickle.load(open(AUTHOR_STATS_WITH_CONTRIBUTION_COUNT, 'rb'))

def append_item_to_list(dictionary, field, item):
    if field in dictionary:
        dictionary[field].append(item)
    else:
        dictionary[field] = [item]

"""
reddit.name.involvements is a list of tuples: (author name, total ups, total comment counts, author score)

involvements sorted by total ups, meaning most succesfully author.
"""
reddit = defaultdict(dict)
ELITE_PERCENTAGE = 0.05

author_count = 0
for author_name, obj in author_stats.iteritems():
    author_count += 1
    if author_count % 200 == 0:
        print "processing no.", author_count
    for reddit_name, ups in obj['contributions'].iteritems(): # currently obj['contributions'] is a list.
        author_this_subreddit_count = obj['contributions_by_count'][reddit_name]
        append_item_to_list(reddit[reddit_name], 'involvements', (author_name, ups, author_this_subreddit_count, obj['mapped_score_by_overlap']))
        reddit[reddit_name]['name'] = reddit_name

for reddit_name, obj in reddit.iteritems():
    involvements = obj['involvements']
    involvements = sorted(involvements, key=lambda tup: tup[1], reverse=True) # sort by [1]: total ups or [2]: total counts.
    counter = 0
    total = len(involvements) * ELITE_PERCENTAGE
    elite_score_lst_overlap = []
    while counter < total:
        elite_score_lst_overlap.append(involvements[counter][3])
        counter += 1
    all_score_lst_overlap = map(lambda x: x[3], involvements)
    if len(elite_score_lst_overlap) > 0:
        aver_elite_overlap = sum(elite_score_lst_overlap) / len(elite_score_lst_overlap)
    else: 
        aver_elite_overlap = -1
    if len(all_score_lst_overlap) > 0:
        aver_all_overlap = sum(all_score_lst_overlap) / len(all_score_lst_overlap)
    else:
        aver_all_overlap = -1
    reddit[reddit_name]['elite_scores_overlap'] = aver_elite_overlap
    reddit[reddit_name]['all_scores_overlap'] = aver_all_overlap

pickle.dump(reddit, open(SUBREDDIT_STATS, 'wb'))
print("saved stats for each subreddit...")