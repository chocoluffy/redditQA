"""
Run `python draw_score/correlation.py` at root folder.
"""

import pickle
import os.path
import csv
from collections import defaultdict
from operator import itemgetter
from scipy.stats import linregress
import math

VERSION_PATH = './models/no_tfidf_topic_100_31G_data'
REDDIT_ALL = os.path.join(VERSION_PATH, 'reddit_all.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, 'complete_author_stats.pkl') # each author's statistics. 
SCORE_ANALYSIS = os.path.join(VERSION_PATH, 'score_analysis.csv')

"""
Global Configuration
"""
KEYWORD = 'entropy' # 'lda'; 'overlap'; 'entropy'
ELITE_PERCENTAGE = 0.05 # meaning pick the top 10% authors as elite users.

common_score = 'scores_by_' + KEYWORD
elite_score = 'elite_scores_' + KEYWORD

"""
Each author's information lookup, contains field:
    - mapped_score
    - mapped_score_by_overlap
    - mapped_score_by_entropy
    - contributions_by_count
    - contributions (by total votes)
"""
author_stats = pickle.load(open(AUTHOR_STATS, 'rb'))
print("author stats loaded...")

score_lda = []
score_overlap = []
score_entropy = []
for author, obj in author_stats.iteritems():
    score_lda.append(obj['mapped_score'])
    score_overlap.append(obj['mapped_score_by_overlap'])
    score_entropy.append(obj['mapped_score_by_entropy'])

lda_overlap = linregress(score_lda, score_overlap)
overlap_entropy = linregress(score_overlap, score_entropy)
lda_entropy = linregress(score_lda, score_entropy)
