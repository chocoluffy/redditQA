import csv
import pickle
from operator import itemgetter
import gensim

author_stats = pickle.load(open("./models/each_author_topic_comments.pkl", 'rb'))

"""
each user(row) has fields ["name", "dom_topics", "score", "contributions", "comments", "subreddit_num"]
"""

def write_dict_data_to_csv_file(csv_file_path, dict_data):
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = dict_data[dict_data.keys()[0]].keys()
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
                else:
                    line.append(value[field])
            writer.writerow(line)
        
    csv_file.close()

# write_dict_data_to_csv_file('results/each_author_topic_comment.csv', author_stats)


import numpy as np
import matplotlib.pyplot as plt

"""
Examine the distribution of dominant topics.
"""
ldamodel = gensim.models.ldamodel.LdaModel.load('models/tfidf.lda')
topic_lst = []
for name, obj in author_stats.iteritems():
    topic_lst.extend(map(lambda x: x[0], obj['dom_topics']))
num_bins = 100
n, bins, patches = plt.hist(topic_lst, num_bins, facecolor='blue', alpha=0.5)

plt.xticks(range(100))
plt.xticks(rotation=45)
plt.show()

