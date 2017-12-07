"""
Produce the subreddit's mapping vector from the overlapping data.

Run:
`python subreddit_map/run.py`
"""

import pandas as pd
import scipy.sparse as ss
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.base import BaseEstimator
from sklearn.utils import check_array
from os.path import isfile
import subprocess
import pickle

CSV_PATH = './overlap_author_2015_till_now'
PICKLE_PATH = './models/subreddit_vector.pkl'

raw_data = pd.read_csv(CSV_PATH)
raw_data.head()


# # group the data by subreddit, then select NumOverlaps and sum those for each group.
# subreddit_popularity = raw_data.groupby('t2_subreddit')['NumOverlaps'].sum()

# # sorting this Series and extracting the index will give us a ranking of subreddits by approximate popularity(sum of all unique commenters).
# # for example, the first one is "AskReddit", and stored as the first entry in subreddits.
# subreddits = np.array(subreddit_popularity.sort_values(ascending=False).index)

# # print subreddits.shape

# # pivot the data into a matrix such that rows and columns are both indexed by subreddits, and the entry at position (i,j) is the number of overlaps bwteen the ith and jth subreddits.
# index_map = dict(np.vstack([subreddits, np.arange(subreddits.shape[0])]).T)

# print raw_data.t2_subreddit.map(index_map)

# # each row of the matrix represents information for each subreddit with others.
# count_matrix = ss.coo_matrix((raw_data.NumOverlaps, 
#                               (raw_data.t2_subreddit.map(index_map),
#                                raw_data.t1_subreddit.map(index_map))),
#                              shape=(subreddits.shape[0], subreddits.shape[0]),
#                              dtype=np.float64)

# # row normalization. 
# conditional_prob_matrix = count_matrix.tocsr()
# conditional_prob_matrix = normalize(conditional_prob_matrix, norm='l1', copy=False)

# # reduce dimension to 500 from 56187 subreddits.
# reduced_vectors = TruncatedSVD(n_components=500,
#                                random_state=1).fit_transform(conditional_prob_matrix)

# reduced_vectors = normalize(reduced_vectors, norm='l2', copy=False)

# # print subreddits[0], reduced_vectors[0]

# res = []

# for name, vec in zip(subreddits, reduced_vectors):
#     res.append((name, vec))

# # save subreddit vectors and labels into pickle for later use.
# pickle.dump(res, open(PICKLE_PATH, 'wb'))