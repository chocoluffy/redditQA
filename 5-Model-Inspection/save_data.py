import csv
import pickle
from operator import itemgetter
import gensim
from gensim import corpora
from collections import defaultdict
from scipy.interpolate import interp1d

# Draw plot.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

# write_dict_data_to_csv_file('models/denorm_200_topic_100/each_author_topic_comment.csv', author_stats)


# Construct dictionary for each reddit.

corpus = corpora.MmCorpus('./models/corpus.mm')
print("document to term matrix loaded...")
ldamodel = gensim.models.ldamodel.LdaModel.load('models/no_tfidf_topic_100/tfidf.lda')
print("lda model loaded...")

# Return all topics probability distribution for each document, instead of clipping value using threshold.
def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    topic_dist = gamma[0] / sum(gamma[0])
    # return [(topic_id, topic_value) for topic_id, topic_value in enumerate(topic_dist)]
    return topic_dist # return direct value

subreddits = []
data = []
commentCounters = []
reddit_comments = pickle.load(open("./models/4G_top008subreddit_top1kcomments.pkl", 'rb'))
print("local comments data loaded...")

for label, obj in reddit_comments.items():
    subreddits.append(label)
    data.append(obj["docset"])
    commentCounters.append(obj["length"])
    
def construct_reddit():
    # Covert the comments from data into a topic vector, for now given 100 topics, each vector will be 
    # of length 100, indicating the probability from each topic.
    reddit_2_topic = defaultdict(dict)
    for index, doc_term_vec in enumerate(corpus):
        topic_dist = get_doc_topics(ldamodel, doc_term_vec)
        reddit_2_topic[subreddits[index]]['topic_dist'] = topic_dist
        reddit_2_topic[subreddits[index]]['doc'] = data[index]
        # topic_dist = ldamodel[doc_term_vec] # Bad, only shows top several topics; it clips the topic value under threshold.

    # populate from author_stats.
    reddit = defaultdict(lambda:defaultdict(list))
    for author_name, obj in author_stats.iteritems():
        for reddit_name, ups in obj['contributions'].iteritems():
            reddit[reddit_name]['involvements'].append((author_name, ups))
            reddit[reddit_name]['scores'].append(obj['mapped_score'])
            reddit[reddit_name]['name'] = reddit_name
    
    # populate from reddit_2_topic
    for reddit_name in reddit.iterkeys():
        if reddit_name in reddit_2_topic:
            topic_vec = reddit_2_topic[reddit_name]['topic_dist']
            filtered_topics = []
            for index, value in enumerate(topic_vec):
                if value > 0.1: # use 0.1 as topic cutoff
                    filtered_topics.append((index, value))
            topic_str = map(lambda x: (topic2str[x[0]], x[1]), filtered_topics)
            topic_str = sorted(topic_str, key=lambda tup: tup[1], reverse=True)
            reddit[reddit_name]['dom_topic_str'] = topic_str
            reddit[reddit_name]['dom_topic'] = filtered_topics
            reddit[reddit_name]['comments'] = reddit_2_topic[reddit_name]['doc']
    return reddit



def subreddit_to_authors_distribution(reddit):
    """
    Given author_stats, make backward counter, generate csv file for each subreddit.
    """
    
    # print reddit
    csv_file_path = 'models/no_tfidf_topic_100/each_subreddit_author_distribution.csv'
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = ['name', 'involvements', 'total_author_count', 'scores', 'dom_topic', 'dom_topic_str']
    writer.writerow(headers)

    for key, value in reddit.items():
        # print key, value
        line = []
        for field in headers:
            if field == 'involvements':
                res = sorted(value['involvements'], key=lambda tup: tup[1], reverse=True)
                line.append(res) 
            elif field == 'total_author_count':
                res = len(value['involvements'])
                line.append(res) 
            elif field == 'scores':
                res = sum(value['scores']) / len(value['scores'])
                line.append(res)
            elif field == 'comments':
                if value['comments']:
                    res =  unicode(value['comments'], "utf-8", errors="ignore")
                    line.append(res)
                else: 
                    line.append(value['comments'])
            else:
                line.append(value[field])
        writer.writerow(line)
        
    csv_file.close()

reddit = construct_reddit()
# print reddit
subreddit_to_authors_distribution(reddit)


def plot_dom_topic_distribution():    
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

    plt.savefig("models/denorm_200_topic_100/topic_dist.png")
    plt.show()