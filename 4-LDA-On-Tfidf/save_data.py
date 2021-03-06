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
import pandas as pd
from collections import defaultdict

"""
Examine the distribution of dominant topics.
"""
ldamodel = gensim.models.ldamodel.LdaModel.load('models/tfidf.lda')
topic_freq = [0] * 100
for name, obj in author_stats.iteritems():
    for topic_tup in obj['dom_topics']:
        topic_freq[topic_tup[0]] += 1

freq_series = pd.Series.from_array(topic_freq)   # in my original code I create a series and run on that, so for consistency I create a series from the list.

x_labels = range(100)

# now to plot the figure...
plt.figure(figsize=(12, 8))
ax = freq_series.plot(kind='bar')
ax.set_title("Dominant Topics Distribution")
ax.set_xlabel("Topic ID")
ax.set_ylabel("Frequency")
ax.set_xticklabels(x_labels)

rects = ax.patches


labels = ["{0}".format(' + '.join(map(lambda x: x[0], ldamodel.show_topic(i, topn=3)))) for i in xrange(len(rects))]

for i, (rect, label) in enumerate(zip(rects, labels)):
    height = rect.get_height()
    if topic_freq[i] > 200:
        ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

plt.savefig("results/topic_dist.png")
plt.show()