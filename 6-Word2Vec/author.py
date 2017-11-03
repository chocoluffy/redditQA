import csv
import pickle
from operator import itemgetter
import gensim
from gensim import corpora
from collections import defaultdict
from scipy.interpolate import interp1d
import os.path

VERSION_PATH = './models/lsi_tfidf_topic_100'
AUTHOR_COMMENT_RAW = os.path.join(VERSION_PATH, 'each_author_topic_comments.pkl')
LDA_MODEL = os.path.join(VERSION_PATH, 'tfidf.lda')
AUTHOR_CSV = os.path.join(VERSION_PATH, 'each_author_topic_comment.csv')

author_stats = pickle.load(open(AUTHOR_COMMENT_RAW, 'rb'))
ldamodel = gensim.models.ldamodel.LdaModel.load(LDA_MODEL)


# import construction from module.
from construct_vec_from_overlap import *

names, name2vec, indexing = construct_mapping_from_overlap()

print compare_two_subreddit_similarity('technology', 'apple', name2vec)

# """
# each user(row) has fields ["name", "dom_topics", "dom_topic_str", "score", "mapped_score", "contributions", "comments", "subreddit_num"]
# """

# # Extract score out for mapping.
# scores = []

# # Add field "dom_topic_str" to the dictionary.
# topic2str = defaultdict(str)
# for i in range(100):
#     topic2str[i] = ' + '.join(map(lambda x: x[0], ldamodel.show_topic(i, topn=4)))

# for name, obj in author_stats.iteritems():
#     topic_str = ["({0}, {1})".format(topic2str[tup[0]], tup[1]) for tup in obj['dom_topics']]
#     author_stats[name]['dom_topics_str'] = topic_str
#     scores.append(obj['score'])

# scale = interp1d([min(scores), max(scores)],[1,100])

# for name, obj in author_stats.iteritems():
#     author_stats[name]['mapped_score'] = scale(obj['score'])

# def write_dict_data_to_csv_file(csv_file_path, dict_data):
#     csv_file = open(csv_file_path, 'wb')
#     writer = csv.writer(csv_file, dialect='excel')
    
#     headers = dict_data[dict_data.keys()[0]].keys()
#     writer.writerow(headers)

#     for key, value in dict_data.items():
#         # print key, value
#         if isinstance(value['subreddit_num'], int): # filter malformed field.
#             line = []
#             for field in headers:
#                 if field == 'contributions':
#                     res = sorted(value['contributions'].iteritems(), key=itemgetter(1), reverse=True)
#                     line.append(res) 
#                 elif field == 'comments':
#                     res = value['comments'][:20]
#                     line.append(res)
#                 else:
#                     line.append(value[field])
#             writer.writerow(line)
        
#     csv_file.close()

# write_dict_data_to_csv_file(AUTHOR_CSV, author_stats)
