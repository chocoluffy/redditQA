
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


raw_data = pd.read_csv('subreddit-overlap.archive')
raw_data.head()


subreddit_popularity = raw_data.groupby('t2_subreddit')['NumOverlaps'].sum()
subreddits = np.array(subreddit_popularity.sort_values(ascending=False).index)


index_map = dict(np.vstack([subreddits, np.arange(subreddits.shape[0])]).T)

count_matrix = ss.coo_matrix((raw_data.NumOverlaps, 
                              (raw_data.t2_subreddit.map(index_map),
                               raw_data.t1_subreddit.map(index_map))),
                             shape=(subreddits.shape[0], subreddits.shape[0]),
                             dtype=np.float64)

conditional_prob_matrix = count_matrix.tocsr()
conditional_prob_matrix = normalize(conditional_prob_matrix, norm='l1', copy=False)


reduced_vectors = TruncatedSVD(n_components=500,
                               random_state=1).fit_transform(conditional_prob_matrix)
reduced_vectors = normalize(reduced_vectors, norm='l2', copy=False)

# print subreddits[0], reduced_vectors[0]

res = []

for name, vec in zip(subreddits, reduced_vectors):
    res.append((name, vec))

# save subreddit vectors and labels into pickle for later use.
pickle.dump(res, open("./subreddit_vector.pkl", 'wb'))