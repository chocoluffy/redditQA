"""
Some tips:
- Make sure use a relatively balanced dataset, each subreddit with 10000 comments. Check the last one's comment count.
- Before training on TF-IDF, need to de-normalize it into normal integer!

Goal:
Finally will save data into each_author_topic_comments.pkl, for further process in author_*.py and subreddit_*.py 

"""
from __future__ import division
import operator
import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path
import re

# Gloabl Configuration
VERSION_PATH = './../models/no_tfidf_topic_100_8G_data'


DICTIONARY_PATH = os.path.join(VERSION_PATH, 'dictionary.dict')
CORPUS_PATH = os.path.join(VERSION_PATH, 'corpus.mm.bz2')
CORPUS_TFIDF_PATH = os.path.join(VERSION_PATH, 'corpus-tfidf.mm')
LDA_PATH = os.path.join(VERSION_PATH, 'model.lda')
TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top25subreddit_top6kcomments.pkl')
AUTHOR_TOPICS = os.path.join(VERSION_PATH, 'author_topics.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, 'each_author_topic_comments.pkl')
AUTHOR_STATS_WITH_CONTRIBUTION_COUNT = os.path.join(VERSION_PATH, 'each_author_topic_comments_with_count.pkl')

TF_IDF = False
MULTI_CORE = True


subreddits = []
data = []
commentCounters = []
# counter = 0

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

# use pymongo to load large chunk of data from mongo.
def load_from_mongo():
    if not os.path.exists(TOP_COMMENTS):
        # Use pymongo to achieve same effect as below codes. 
        pipe = [
            {'$sort': {"ups": -1 }}, # sort before grouping, so that the comments array is sorted in order.
            {'$group': {'_id': '$subreddit', 'comments': { '$push':  { 'body': "$body", 'ups': "$ups" } }}},
            {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
            { "$project": { 
                "comments": { "$slice": [ "$comments", 2500 ] }, # slice the top comments.
                "commentsCount": 1
            }},
            {"$sort": {"commentsCount": -1}},
            {"$out" : "top_comments" }
        ]

        sub_data = defaultdict(dict)
        counter = 0
        cursor = db.docs_l8.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = db.top_comments.find({}).count()
        print("totoal count...", total_count)
        for document in db.top_comments.find({}):
            counter += 1
            if counter < total_count * 0.33: # only use the top most active subreddit data.
                print "Processing #%d subreddit"%(counter)
                docset = " ".join(map(lambda x: x["body"], document['comments']))
                sub_data[document['_id']]['docset'] = docset
                sub_data[document['_id']]['length'] = document['commentsCount']
        print("local comments data saved...")
        pickle.dump(sub_data, open(TOP_COMMENTS, 'wb'))
        for label, obj in sub_data.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])
    else:
        reddit_comments = pickle.load(open(TOP_COMMENTS, 'rb'))
        print("local comments data loaded...")
        for label, obj in reddit_comments.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])


load_from_mongo()

# compile documents
doc_complete = data

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
import string
import gensim
from gensim import corpora
import os.path
import bz2

# If dictionary model exists, use it; Otherwise, save a new one.
if not os.path.exists(DICTIONARY_PATH):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    # Remove stopwords, punctuation, links, numbers, long words(>20), and normalize them.
    def clean(doc):
        link_free = re.sub(r"http\S+", "", doc) # remove url
        hashtag_free = " ".join(re.findall('[A-Z][^A-Z]*', link_free)) # remove hashtag style words, such as: OnePieceIsGreat
        number_free = re.sub(r'\d+', "", hashtag_free) # remove numbers
        specialchar_free = re.sub(r'[^\x00-\x7f]',r' ', number_free) # remove non-english characters
        specialchar_free = re.sub( '\s+', ' ', specialchar_free ).strip() # replace multiple space with one
        stop_free = " ".join([i for i in specialchar_free.lower().split() if i not in stop and len(i) > 2 and len(i) < 20]) # remove stopword
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude) # remove punctuation
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split()) # stem
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete] 

    # Add bigrams that appear 100 times or more.
    bigram = Phrases(doc_clean, min_count=100)
    for idx in range(len(doc_clean)):
        for token in bigram[doc_clean[idx]]: 
            if '_' in token:
                doc_clean[idx].append(token)

    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # Filter out words that occur less than 30 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=30, no_above=0.5)
    dictionary.save(DICTIONARY_PATH)
else:
    dictionary = corpora.Dictionary.load(DICTIONARY_PATH)
    print("preprocessed ictionary loaded...")


if not os.path.exists(CORPUS_PATH):
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above. [Bag Of Word]
    corpus = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Save the matrix into Market Matrix format. 
    corpora.MmCorpus.serialize(CORPUS_PATH, corpus)
else:
    # corpus = corpora.MmCorpus(CORPUS_PATH)
    corpus = corpora.MmCorpus(bz2.BZ2File(CORPUS_PATH)) # use bz2 version.
    print("document to term matrix loaded...")

# Use TF-IDF model
if TF_IDF:
    if not os.path.exists(CORPUS_TFIDF_PATH):
        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above. [Bag Of Word]
        tfidf = gensim.models.TfidfModel(corpus, normalize=True)
        corpus_tfidf = tfidf[corpus]
        print("de-normaliza tf-idf corpus...")
        # corpus_tfidf = map(lambda x: map(lambda y: (y[0], round(y[1] * 200, 1)), x), corpus_tfidf)
        # Save the matrix into Market Matrix format. 
        corpora.MmCorpus.serialize(CORPUS_TFIDF_PATH, corpus_tfidf)
    else:
        corpus_tfidf = corpora.MmCorpus(CORPUS_TFIDF_PATH)
        print("tfidf version of document to term matrix loaded...")


# def print_corpus_word_weight(tfidf = True):
#     if tfidf:
#         print("tfidf weights of the first document after de-normalization")
#         pprint(map(lambda x: (dictionary[x[0]], x[1]), corpus_tfidf[0]))
#     else:
#         print("BOW of the first document")
#         pprint(map(lambda x: (dictionary[x[0]], x[1]), corpus[0]))


# print_corpus_word_weight(tfidf = False)
# pprint(len(corpus[0]))

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Save LDA model
if not os.path.exists(LDA_PATH):
    # Creating the object for LDA model using gensim library
    if MULTI_CORE:
        Lda = gensim.models.ldamulticore.LdaMulticore
    else:
        Lda = gensim.models.ldamodel.LdaModel
    # Running and Trainign LDA model on the document term matrix.
    if TF_IDF:
        ldamodel = Lda(corpus_tfidf, num_topics=100, id2word = dictionary, passes=50, workers=20)
    else:
        ldamodel = Lda(corpus, num_topics=100, id2word = dictionary, passes=50, workers=20)
    ldamodel.save(LDA_PATH)
else:
    ldamodel = gensim.models.ldamodel.LdaModel.load(LDA_PATH)
    print("lda model loaded...")



def print_general_subreddit_topic():
    """
    Print all 100 topics for human inspection.
    """
    ldamodel.print_topics(100)

def print_specific_subreddit_topic(id):
    print ldamodel.show_topic(id, topn=10)

print_general_subreddit_topic()
# print_specific_subreddit_topic(22)


# Return all topics probability distribution for each document, instead of clipping value using threshold.
def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    topic_dist = gamma[0] / sum(gamma[0])
    # return [(topic_id, topic_value) for topic_id, topic_value in enumerate(topic_dist)]
    return topic_dist # return direct value


# Covert the comments from data into a topic vector, for now given 100 topics, each vector will be 
# of length 100, indicating the probability from each topic.
rc_tvec = []
if TF_IDF:
    for doc_term_vec in corpus_tfidf:
        topic_dist = get_doc_topics(ldamodel, doc_term_vec)
        rc_tvec.append(topic_dist)
        # topic_dist = ldamodel[doc_term_vec] # Bad, only shows top several topics; it clips the topic value under threshold.
else:
    for doc_term_vec in corpus:
        topic_dist = get_doc_topics(ldamodel, doc_term_vec)
        rc_tvec.append(topic_dist)

# # Below are tasks utilizing the above model.


# pprint(rc_tvec)
# Print the topic-words distribution for some specific topics.
def print_specific_subreddit_topic():    
    dominant_counter = 0
    for label, topic_dist_vec in zip(subreddits, rc_tvec):
        filtered_topics = []
        for index, value in enumerate(topic_dist_vec):
            if value > 0.1: # use 0.1 as topic cutoff
                filtered_topics.append((index, value))
        # index, value = max(enumerate(topic_dist_vec), key=operator.itemgetter(1))
        if label in ["MMA", "guns", "DIY", "DotA2", "toronto", "cats", "food", "nba"]:
            print "For subreddit: ", label
            # print "its topic distribution vector: ", topic_dist_vec
            print "the dominant topic is: ", filtered_topics, map(lambda x: ldamodel.show_topic(x[0], topn=5), filtered_topics)
        if value > 0.5:
            dominant_counter += 1
    print "From ", len(subreddits), " all subreddit, ", dominant_counter, " of all owns a dominant topics"

# print_specific_subreddit_topic()



def find_dom_topic_vec(name):
    """
    Assume a subreddit can be represented by its most dominant topic vector. (currently ignore less dominant topics, 
    as one subreddit can cover several topics). 
    if name not appear in the subreddits list(all subreddit label from data), return -1.
    """
    if name not in subreddits:
        print("subreddit not in list...")
        return []
    else:
        subreddits_index = subreddits.index(name)
        topic_vec = rc_tvec[subreddits_index]
        # dom_topic_index, prob = max(enumerate(topic_vec), key=operator.itemgetter(1))
        # filtered_topics = []
        # for index, value in enumerate(topic_vec):
        #     # if value > 0.1: # use 0.1 as topic cutoff
        #     filtered_topics.append((index, value))
        # return filtered_topics
        return topic_vec


def load_author_from_mongo():
    # use pymongo to load large chunk of data from mongo.
    if not os.path.exists(AUTHOR_TOPICS):
        # Use pymongo to achieve same effect as below codes.
        pipe = [
            {'$group': {
                '_id': '$author',
                'contributions': { '$push':  { 'subreddit': "$subreddit", 'ups': "$ups" } },
                'subredditset': {'$addToSet': "$subreddit"}
            }},
            {'$addFields': { 'subredditnum': { '$size': "$subredditset" } } },
            {'$addFields': { 'commentsCount': { '$size': "$contributions" } } },
            { "$project": { 
                "subredditset": 0
            }},
            {'$match': {
                '$and': [ 
                    {'subredditnum': {'$gt': 5}},
                    {'commentsCount': {'$lt': 1000}}
                ]}
            },
            {"$sort": {"commentsCount": -1}}
        ]

        cursor = db.docs_l8.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = len(list(cursor)) 

        data = defaultdict(dict)
        counter = 0
        for document in db.docs_l8.aggregate(pipeline = pipe, allowDiskUse = True):
            counter += 1
            # Pick the top 33% most acitve user by commentsCount, ignore the first 10, probably bots!
            if counter > 15 and counter < total_count * 0.33:
                print "Processing #%d author"%(counter)
                reddit_ups_data = defaultdict(int)
                for reddit in document['contributions']:
                    reddit_ups_data[reddit['subreddit']] += 1 # use reddit["ups"] or simply 1?
                reddit_dom_topic_vec = defaultdict(dict)
                for name in reddit_ups_data.iterkeys(): # subreddit's name
                    if len(find_dom_topic_vec(name)) > 0: # only store the existing subreddit.
                        reddit_dom_topic_vec[name] = find_dom_topic_vec(name)
                
                data[document['_id']]['contributions'] = reddit_ups_data
                data[document['_id']]['topicvecs'] = reddit_dom_topic_vec
                # print(data)


        pickle.dump(data, open(AUTHOR_TOPICS, 'wb'))
        return data
    else:
        data = pickle.load(open(AUTHOR_TOPICS, 'rb'))
        print("author topics model loaded...")
        return data


author_topics = load_author_from_mongo()


"""
Below are calculating pairwise topic similarity.
"""

import numpy as np
from scipy.spatial.distance import pdist, squareform
import itertools

def hellinger(X):
    return squareform(pdist(np.sqrt(X)))/np.sqrt(2)

X = ldamodel.state.get_lambda()
X = X / X.sum(axis=1)[:, np.newaxis] # normalize vector
h = hellinger(X)

# book = dict(zip(subreddits, range(len(subreddits)))) # a dictionary map subreddit name to its 

inspect_authors_stats = []
for author, obj in author_topics.items():
    """
    First filter by weight cutoff T = 4, remove subreddit contributions less than T.
    obj {
        'topicvecs': {
            'nba': [],  //100 length, topic probability distribution vector.
            ...
        },
        'contributions': {
            'nba': 200,
            ...
        }
    }
    """
    topic_dist_vec = []
    weights = []
    for name in obj['topicvecs'].iterkeys():
        topic_dist_vec.append(obj['topicvecs'][name])
        weights.append(obj['contributions'][name]) # use contribution counts, not sum of ups!
    aver_topic_dist = np.dot(np.asarray(weights), np.asarray(topic_dist_vec)) / sum(weights)
    topic_cut_off = 0.08 # only investigate topic with prob higher than 0.08
    res = []
    for index, value in enumerate(aver_topic_dist):
        if value > topic_cut_off:
            res.append((index, value))
    # print("User author {0}, dominant topics {1}".format(author, res))

    score = 0
    comb = list(itertools.combinations(map(lambda x: x[0], res), 2)) # return topic index permutation.
    if len(comb) > 0:
        for topic_id1, topic_id2 in comb:
            score += (1 - h[topic_id1, topic_id2]) # 1 - Hellinger Distance = simularity
        score = score / len(comb)
        # print(comb)
        # if score > 0.25: # human inspection those specialist!
        # if author == "deweymm":
        # print("User author {0}, dominant topics num {1}, score: {2}, {3}".format(author, len(res), score, res))
        inspect_authors_stats.append((author, res, score))

"""
Up to here: inspect_authors_stats contains the score by LDA. 
In order to construct a complete dictionary file, find to look up from the DB again.
"""

author_stats = defaultdict(dict)
for (name, res, score) in inspect_authors_stats:
    author_stats[name] = defaultdict(dict)
    author_stats[name]['name'] = name
    author_stats[name]['dom_topics'] = res
    author_stats[name]['score'] = score

def collect_authors_info(author_dict):
    """
    Given user's dictionary, save its info into it.
    """
    pipe = [
        {'$sort': {'ups': -1}},
        {'$group': {
            '_id': '$author',
            'contributions': { '$push':  { 'subreddit': "$subreddit", 'ups': "$ups" } },
            'subredditset': {'$addToSet': "$subreddit"},
            'comments': {'$addToSet': "$body"}
        }},
        {'$addFields': { 'subredditnum': { '$size': "$subredditset" } } },
        {'$addFields': { 'commentsCount': { '$size': "$contributions" } } },
        { "$project": { 
            "subredditset": 0
        }},
        {'$match': {
            '$and': [ 
                {'subredditnum': {'$gt': 5}},
                {'commentsCount': {'$lt': 1000}}
            ]}
        },
        {"$sort": {"commentsCount": -1}}
    ]

    for document in db.docs_l8.aggregate(pipeline = pipe, allowDiskUse = True):
        author_name = document['_id']
        if author_name in author_dict:
            contributions = defaultdict(int)
            contributions_by_count = defaultdict(int)
            for comment_info in document['contributions']:
                contributions[comment_info['subreddit']] += comment_info['ups']
                contributions_by_count[comment_info['subreddit']] += 1
            author_stats[author_name]['contributions'] = contributions
            author_stats[author_name]['contributions_by_count'] = contributions_by_count
            author_stats[author_name]['comments'] = document['comments']
            author_stats[author_name]['subreddit_num'] = document['subredditnum']



collect_authors_info(author_stats)
pickle.dump(author_stats, open(AUTHOR_STATS_WITH_CONTRIBUTION_COUNT, 'wb'))
print("saved stats for each user...")