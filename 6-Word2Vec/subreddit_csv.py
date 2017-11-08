from __future__ import division
import csv
import pickle
from operator import itemgetter
import gensim
from gensim import corpora
from collections import defaultdict
from scipy.interpolate import interp1d
import os.path

# Draw plot.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Gloabl Configuration
VERSION_PATH = './models/no_tfidf_topic_100_8G_data'
DICTIONARY_PATH = os.path.join(VERSION_PATH, 'dictionary.dict')
CORPUS_PATH = os.path.join(VERSION_PATH, 'corpus.mm')
CORPUS_TFIDF_PATH = os.path.join(VERSION_PATH, 'corpus-tfidf.mm')
LDA_PATH = os.path.join(VERSION_PATH, 'model.lda')
TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments.pkl')
AUTHOR_TOPICS = os.path.join(VERSION_PATH, 'author_topics.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, 'each_author_topic_comments.pkl')
SUBREDDIT_CSV = os.path.join(VERSION_PATH, 'new_subreddit.csv')



author_stats = pickle.load(open(AUTHOR_STATS, 'rb'))
ldamodel = gensim.models.ldamodel.LdaModel.load(LDA_PATH)


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

# Construct dictionary for each reddit.
corpus = corpora.MmCorpus(CORPUS_PATH)
print("document to term matrix loaded...")

# Return all topics probability distribution for each document, instead of clipping value using threshold.
def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    topic_dist = gamma[0] / sum(gamma[0])
    # return [(topic_id, topic_value) for topic_id, topic_value in enumerate(topic_dist)]
    return topic_dist # return direct value

subreddits = []
data = []
commentCounters = []
reddit_comments = pickle.load(open(TOP_COMMENTS, 'rb'))
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

def subreddit_elite_score(reddit):
    # Try calculating the top 5% elite's average score.
    ELITE_PERCENTAGE = 0.05
    for reddit_name, obj in reddit.iteritems():
        involvements = obj['involvements']
        involvements = sorted(involvements, key=lambda tup: tup[1], reverse=True)
        counter = 0
        total = len(involvements) * ELITE_PERCENTAGE
        score_lst = []
        while counter < total:
            if involvements[counter][0] in author_stats:
                score_lst.append(author_stats[involvements[counter][0]]['mapped_score'])
            counter += 1
        # print reddit_name, score_lst
        aver = sum(score_lst) / len(score_lst)
        reddit[reddit_name]['elite_scores'] = aver
    return reddit


def subreddit_to_authors_distribution(reddit):
    """
    Given author_stats, make backward counter, generate csv file for each subreddit.
    """
    
    # print reddit
    csv_file_path = SUBREDDIT_CSV
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = ['name', 'involvements', 'total_author_count', 'scores', 'elite_scores', 'dom_topic', 'dom_topic_str']
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
reddit = subreddit_elite_score(reddit)
# print reddit
subreddit_to_authors_distribution(reddit)