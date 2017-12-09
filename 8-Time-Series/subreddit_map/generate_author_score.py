"""
Given author stats on its contributions. 

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

VERSION_PATH = './models/201301'
SUBREDDIT_VEC = './models/subreddit_vector_2013.pkl'
AUTHOR_STATS_WITH_CONTRIBUTION_COUNT = os.path.join(VERSION_PATH, 'author_comments_stats_with_score.pkl')

map_vectors = pickle.load(open(SUBREDDIT_VEC, 'rb'))
names_lst, vectors_lst = [list(t) for t in zip(*map_vectors)]
subreddit2vec = defaultdict()
for name, vec in map_vectors:
    subreddit2vec[name] = vec

pair2sim = defaultdict()
def compare_two_subreddit_similarity(name1, name2, name2vec):
    """
    Construct a dictionary to cache the final similarity results. Sort two names and concat as the key.
    """
    if name1 in name2vec and name2 in name2vec:
        pair_key = ','.join(sorted([name1, name2]))
        sub_vec1 = name2vec[name1]
        sub_vec2 = name2vec[name2]
        sub_vec1 = np.array(sub_vec1).reshape((1, len(sub_vec1)))
        sub_vec2 = np.array(sub_vec2).reshape((1, len(sub_vec2)))
        if pair_key in pair2sim:
            res = pair2sim[pair_key]
        else:
            res = cosine_similarity(sub_vec1, sub_vec2)
            # print("add key", pair_key)
            pair2sim[pair_key] = res
        return res
    else:
        # print("at least one of the subreddit not found...")
        return [[-1]]

def return_gs_score_by_overlap(author_stats, subreddit2vec):
    scores_by_overlap = []
    for name, obj in author_stats.iteritems():
        active_contributions = [(i, j) for i,j in obj['contributions_by_count'].iteritems() if j > 1]
        score_by_overlap = 0
        valid_scores = 0
        comb = list(itertools.combinations(active_contributions, 2)) # return topic index permutation.
        if len(comb) > 0:
            for sub1, sub2 in comb:
                # print sub1, sub2, compare_two_subreddit_similarity(sub1, sub2, name2vec)
                weight = math.sqrt(sub1[1] * sub2[1])
                sim = compare_two_subreddit_similarity(sub1[0], sub2[0], subreddit2vec)[0][0]
                # print(sub1, sub2, sim)
                if sim > -1:
                    score_by_overlap += weight * sim # cosine similarity
                    valid_scores += weight
            if valid_scores > 0:
                score_by_overlap = score_by_overlap / valid_scores
        author_stats[name]['score_by_overlap'] = score_by_overlap
        scores_by_overlap.append(score_by_overlap)

    # create scale to map scores_by_overlap to [1, 100].
    scale_by_overlap = interp1d([min(scores_by_overlap), max(scores_by_overlap)],[1,100])

    for name, obj in author_stats.iteritems():
        author_stats[name]['mapped_score_by_overlap'] = scale_by_overlap(obj['score_by_overlap'])

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test


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

author_stats = defaultdict(dict)
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

return_gs_score_by_overlap(author_stats, subreddit2vec)

pickle.dump(author_stats, open(AUTHOR_STATS_WITH_CONTRIBUTION_COUNT, 'wb'))
print("saved stats for each user...")