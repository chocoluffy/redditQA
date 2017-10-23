"""
Some tips:
- Make sure use a relatively balanced dataset, each subreddit with 10000 comments. Check the last one's comment count.
- Before training on TF-IDF, need to de-normalize it into normal integer!
"""
from __future__ import division
import operator
import json
from pprint import pprint
from pymongo import MongoClient
import pickle
from collections import defaultdict
import os.path


subreddits = []
data = []
commentCounters = []
# counter = 0

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

# 898 subreddit with >100 ups comments concated, from rc-2015-06 10G data.
def load_from_file():
    with open('3-results-20170921-224241.json') as f:
        for line in f:
            obj = json.loads(line)
            subreddits.append(obj["subreddit"])
            data.append(obj["comments"])
            commentCounters.append(obj["countcomments"])

# use pymongo to load large chunk of data from mongo.
def load_from_mongo():
    if not os.path.exists('./models/4G_top008subreddit_top1kcomments.pkl'):
        # Use pymongo to achieve same effect as below codes. 
        pipe = [
            {'$sort': {"ups": -1 }}, # sort before grouping, so that the comments array is sorted in order.
            {'$group': {'_id': '$subreddit', 'comments': { '$push':  { 'body': "$body", 'ups': "$ups" } }}},
            {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
            { "$project": { 
                "comments": { "$slice": [ "$comments", 1000 ] }, # slice the top 100 comments.
                "commentsCount": 1
            }},
            {"$sort": {"commentsCount": -1}}
        ]

        sub_data = defaultdict(dict)
        counter = 0
        cursor = db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = len(list(cursor))
        print("totoal count...", total_count)
        for document in db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True):
            counter += 1
            if counter < total_count * 0.08: # only use the top 8% most active subreddit data.
                print "Processing #%d subreddit"%(counter)
                docset = " ".join(map(lambda x: x["body"], document['comments']))
                sub_data[document['_id']]['docset'] = docset
                sub_data[document['_id']]['length'] = document['commentsCount']
        print("local comments data saved...")
        pickle.dump(sub_data, open("./models/4G_top008subreddit_top1kcomments.pkl", 'wb'))
        for label, obj in sub_data.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])
    else:
        reddit_comments = pickle.load(open("./models/4G_top008subreddit_top1kcomments.pkl", 'rb'))
        print("local comments data loaded...")
        for label, obj in reddit_comments.items():
            subreddits.append(label)
            data.append(obj["docset"])
            commentCounters.append(obj["length"])


load_from_mongo()

# print(commentCounters[0], commentCounters[-1])
# print(max(commentCounters), min(commentCounters))


# compile documents

# doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
# doc2 = "My father spends a lot of time driving my sister around to dance practice."
# doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
# doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
# doc5 = "Health experts say that Sugar is not good for your lifestyle."

# compile documents
doc_complete = data

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
import string
import gensim
from gensim import corpora
import os.path

# If dictionary model exists, use it; Otherwise, save a new one.
if not os.path.exists('./models/dictionary.dict'):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation) 
    lemma = WordNetLemmatizer()

    # Remove stopwords, punctuation and normalize them.
    def clean(doc):
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop and len(i) > 1])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    doc_clean = [clean(doc).split() for doc in doc_complete] 

    # Add bigrams that appear 20 times or more.
    bigram = Phrases(doc_clean, min_count=20)
    for idx in range(len(doc_clean)):
        for token in bigram[doc_clean[idx]]: 
            if '_' in token:
                doc_clean[idx].append(token)

    # Creating the term dictionary of our courpus, where every unique term is assigned an index. 
    dictionary = corpora.Dictionary(doc_clean)
    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5)
    dictionary.save('./models/dictionary.dict')
else:
    dictionary = corpora.Dictionary.load('./models/dictionary.dict')
    print("preprocessed ictionary loaded...")


if not os.path.exists('./models/corpus.mm'):
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above. [Bag Of Word]
    corpus = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Save the matrix into Market Matrix format. 
    corpora.MmCorpus.serialize('./models/corpus.mm', corpus)
else:
    corpus = corpora.MmCorpus('./models/corpus.mm')
    print("document to term matrix loaded...")

# Use TF-IDF model
tfidf = gensim.models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

print("de-normaliza tf-idf corpus...")
corpus_tfidf = map(lambda x: map(lambda y: (y[0], round(y[1] * 200, 1)), x), corpus_tfidf)

# pprint(dictionary[237])
print("tfidf weights of the first document after de-normalization")
# print("BOW of the first document")
# pprint(map(lambda x: (dictionary[x[0]], x[1]), corpus[0]))
# pprint(len(corpus[0]))

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Save LDA model
if not os.path.exists('./models/tfidf.lda'):
    # Creating the object for LDA model using gensim library
    Lda = gensim.models.ldamodel.LdaModel
    # Running and Trainign LDA model on the document term matrix.
    ldamodel = Lda(corpus_tfidf, num_topics=100, id2word = dictionary, passes=50)
    ldamodel.save('./models/tfidf.lda')
else:
    ldamodel = gensim.models.ldamodel.LdaModel.load('models/tfidf.lda')
    print("lda model loaded...")



def print_general_subreddit_topic():
    """
    Print all 100 topics for human inspection.
    """
    ldamodel.print_topics(100)

# print_general_subreddit_topic()


# Return all topics probability distribution for each document, instead of clipping value using threshold.
def get_doc_topics(lda, bow):
    gamma, _ = lda.inference([bow])
    topic_dist = gamma[0] / sum(gamma[0])
    # return [(topic_id, topic_value) for topic_id, topic_value in enumerate(topic_dist)]
    return topic_dist # return direct value


# Covert the comments from data into a topic vector, for now given 100 topics, each vector will be 
# of length 100, indicating the probability from each topic.
rc_tvec = []
for doc_term_vec in corpus_tfidf:
    topic_dist = get_doc_topics(ldamodel, doc_term_vec)
    rc_tvec.append(topic_dist)
    # topic_dist = ldamodel[doc_term_vec] # Bad, only shows top several topics; it clips the topic value under threshold.
    


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

print_specific_subreddit_topic()



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
    if not os.path.exists('./models/author_topics.pkl'):
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

        cursor = db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True)
        total_count = len(list(cursor)) 

        data = defaultdict(dict)
        counter = 0
        for document in db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True):
            counter += 1
            # Pick the top 5% most acitve user by commentsCount, ignore the first 10, probably bots!
            if counter > 10 and counter < total_count * 0.05:
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


        pickle.dump(data, open("./models/author_topics.pkl", 'wb'))
        return data
    else:
        data = pickle.load(open("./models/author_topics.pkl", 'rb'))
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
        weights.append(obj['contributions'][name])
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

    for document in db.docs_l4.aggregate(pipeline = pipe, allowDiskUse = True):
        author_name = document['_id']
        if author_name in author_dict:
            contributions = defaultdict(int)
            for comment_info in document['contributions']:
                contributions[comment_info['subreddit']] += comment_info['ups']
            author_stats[author_name]['contributions'] = contributions
            author_stats[author_name]['comments'] = document['comments']
            author_stats[author_name]['subreddit_num'] = document['subredditnum']



collect_authors_info(author_stats)
pickle.dump(author_stats, open("./models/each_author_topic_comments.pkl", 'wb'))
print("saved stats for each user...")



# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import numpy as np
# from adjustText import adjust_text
# import math

# def plot_specialist_distribution():
#     """
#     x: each subreddit average generalist/specialist scores.
#     y: avg contribution (within 4 days)
#     radius: how many authors involved.

#     inspect_authors_stats: each tuple contains author, res, score
#     data: each author's contribution.
#     """
#     reddit = defaultdict(list)
#     author_scores = defaultdict(dict)
#     res = defaultdict(dict)
#     for name, res, score in inspect_authors_stats:
#         author_scores[name] = score

#     for author in author_topics.iterkeys():
#         for subreddit in author_topics[author]['contributions']:
#             if author_scores[author]:
#                 reddit[subreddit].append((author_scores[author], author_topics[author]['contributions'][subreddit], 1))

#     labels = []
#     x = []
#     y = []
#     r = []
#     # pprint(reddit)
#     for subreddit, lst in reddit.iteritems():
#         labels.append(subreddit)
#         x.append(sum(map(lambda x: x[0], lst)) / len(lst))
#         y.append(sum(map(lambda x: x[1], lst)) / len(lst))
#         r.append(sum(map(lambda x: x[2], lst)))
    
#     print(r)
#     colors = cm.rainbow(np.linspace(0, 1, len(labels)))
                   
#     fig = plt.figure(figsize=(16, 16)) 
#     ax = fig.add_subplot(111)
#     fig.subplots_adjust(top=0.85)
#     ax.set_xlabel('generalist/specialist score')
#     ax.set_ylabel('average contributions count')

#     for i in range(len(x)):
#         sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 20), linewidths=2, edgecolor='w')
#         sct.set_alpha(0.75)
#         if float(y[i]) > 15:
#             plt.annotate(labels[i],
#                         xy=(x[i], y[i]),
#                         xytext=(5, 2),
#                         textcoords='offset points',
#                         ha='right',
#                         va='bottom')
#     plt.show()

# # plot_specialist_distribution()


# # print_authors_comments(inspect_authors_stats)

# # # # print_general_subreddit_topic()

