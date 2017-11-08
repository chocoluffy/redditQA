# combine stats from author.py on 4G data and 8G data.

from __future__ import division # to force division be float.
import csv
import pickle
from operator import itemgetter
import gensim
from gensim import corpora
from collections import defaultdict
from scipy.interpolate import interp1d
import os.path
import itertools
import math

# Model path.
# VERSION_PATH = './models/lsi_tfidf_topic_100'
VERSION_PATH = './models/no_tfidf_topic_100_combine_data'

AUTHOR_COMMENT_RAW = os.path.join(VERSION_PATH, 'each_author_topic_comments.pkl')
LDA_MODEL = os.path.join(VERSION_PATH, 'model.lda')
AUTHOR_CSV = os.path.join(VERSION_PATH, 'each_author_topic_comment.csv')

author_stats = pickle.load(open(AUTHOR_COMMENT_RAW, 'rb'))
ldamodel = gensim.models.ldamodel.LdaModel.load(LDA_MODEL)


# import construction from module.
from construct_vec_from_overlap import *

names, name2vec, indexing = construct_mapping_from_overlap()

# import 8G author_stats from module.
from author import *

author_stats_large = return_author_stats_on_8G()



"""
each user(row) has fields ["name", "dom_topics", "dom_topic_str", "score", "mapped_score", "contributions", "comments", "subreddit_num"]
"""

# Extract score out for mapping.
scores = []

# Add field "dom_topic_str" to the dictionary.
topic2str = defaultdict(str)
for i in range(100):
    topic2str[i] = ' + '.join(map(lambda x: x[0], ldamodel.show_topic(i, topn=4)))

for name, obj in author_stats.iteritems():
    topic_str = ["({0}, {1})".format(topic2str[tup[0]], tup[1]) for tup in obj['dom_topics']]
    author_stats[name]['dom_topics_str'] = topic_str
    scores.append(obj['score'])

scale = interp1d([min(scores), max(scores)],[1,100])

# Add mapped_score, score_by_overlap, mapped_score_by_overlap into the object.
scores_by_overlap = []

# sim_names, sim_matrix = compare_subreddits_similarity_batch(name2vec)
# print sim_names, sim_matrix

for name, obj in author_stats.iteritems():
    author_stats[name]['mapped_score'] = scale(obj['score'])
    active_contributions = [(i, j) for i,j in obj['contributions'].iteritems() if j > 1]
    # active_contributions = filter(lambda x: x[1] > 1, obj['contributions']) # filter those minute contributions.
    # print active_contributions
    score_by_overlap = 0
    valid_scores = 0
    comb = list(itertools.combinations(active_contributions, 2)) # return topic index permutation.
    if len(comb) > 0:
        for sub1, sub2 in comb:
            # print sub1, sub2, compare_two_subreddit_similarity(sub1, sub2, name2vec)
            weight = math.sqrt(sub1[1] * sub2[1])
            sim = compare_two_subreddit_similarity(sub1[0], sub2[0], name2vec)[0][0]
            # print(sub1, sub2, sim)
            if sim > -1:
                score_by_overlap += weight * sim # cosine similarity
                valid_scores += weight
        score_by_overlap = score_by_overlap / valid_scores
    author_stats[name]['score_by_overlap'] = score_by_overlap
    # print(name, score_by_overlap)
    scores_by_overlap.append(score_by_overlap)


scale_by_overlap = interp1d([min(scores_by_overlap), max(scores_by_overlap)],[1,100])
for name, obj in author_stats.iteritems():
    author_stats[name]['mapped_score_by_overlap'] = scale_by_overlap(obj['score_by_overlap'])
    if author_stats[name]['mapped_score_by_overlap'] == 1:
        author_stats[name]['mapped_score_by_overlap'] = -1 # meaning data too few.


def write_dict_data_to_csv_file(csv_file_path, dict_data):
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = dict_data[dict_data.keys()[0]].keys()
    new_headers = ['8g_mapped_score', '8g_mapped_score_by_overlap', '8g_dom_topics_str', '8g_contributions', '8g_subreddit_num']
    # print headers
    headers.extend(new_headers)
    
    writer.writerow(headers)

    for key, value in dict_data.items():
        # print key, value
        if isinstance(value['subreddit_num'], int): # filter malformed field.
            line = []
            for field in headers:
                if field == 'contributions':
                    res = sorted(value['contributions'].iteritems(), key=itemgetter(1), reverse=True)
                    line.append(res) 
                elif field == 'comments':
                    res = value['comments'][:20]
                    line.append(res)
                elif field in new_headers: # add the data from 8g dictionary.
                    origin_name = '_'.join(field.split('_')[1:])
                    if key in author_stats_large:
                        if origin_name in author_stats_large[key]:
                            res = author_stats_large[key][origin_name]
                            line.append(res)
                        else:
                            line.append([])
                    else:
                        line.append([])
                else:
                    line.append(value[field])
            writer.writerow(line)
        
    csv_file.close()

write_dict_data_to_csv_file(AUTHOR_CSV, author_stats)



# For now, author_stats contains stats from 8G data.
