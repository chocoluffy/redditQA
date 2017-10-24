import csv
import pickle
from operator import itemgetter
import gensim
from collections import defaultdict
from scipy.interpolate import interp1d

author_stats = pickle.load(open("./models/no_tfidf_topic_100/each_author_topic_comments.pkl", 'rb'))
ldamodel = gensim.models.ldamodel.LdaModel.load('models/no_tfidf_topic_100/tfidf.lda')

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

for name, obj in author_stats.iteritems():
    author_stats[name]['mapped_score'] = scale(obj['score'])

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

write_dict_data_to_csv_file('models/no_tfidf_topic_100/each_author_topic_comment.csv', author_stats)


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


"""
Examine the distribution of dominant topics.
"""
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

plt.savefig("models/no_tfidf_topic_100/topic_dist.png")
plt.show()