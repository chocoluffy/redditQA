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
import re

# Gloabl Configuration
VERSION_PATH = './models/lsi_tfidf_topic_100'
DICTIONARY_PATH = os.path.join(VERSION_PATH, 'dictionary.dict')
CORPUS_PATH = os.path.join(VERSION_PATH, 'corpus.mm')
CORPUS_TFIDF_PATH = os.path.join(VERSION_PATH, 'corpus-tfidf.mm')
LSI_PATH = os.path.join(VERSION_PATH, 'model.lsi')
LSI_INDEX = os.path.join(VERSION_PATH, 'lsi.index')
MAP_VECTORS_FROM_OVERLAP = os.path.join(VERSION_PATH, 'subreddit_vector.pkl')
OVERLAP_INDEX = os.path.join(VERSION_PATH, 'overlap.index')
TF_IDF = True
NUM_TOPICS = 200
NUM_FEATURES_OVERLAP = 500


subreddits = []
data = []
commentCounters = []
# counter = 0

# Mongo config.
con = MongoClient('localhost', 27017)
db = con.test

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

# compile documents
doc_complete = data

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
import string
import gensim
from gensim import corpora, similarities
import os.path

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
        stop_free = " ".join([i for i in number_free.lower().split() if i not in stop and len(i) > 1 and len(i) < 20]) # remove stopword
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude) # remove punctuation
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split()) # stem
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
    corpus = corpora.MmCorpus(CORPUS_PATH)
    print("document to term matrix loaded...")

# Use TF-IDF model
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



import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Save LSI model
if not os.path.exists(LSI_PATH):
    # Creating the object for LSI model using gensim library
    Lsi = gensim.models.lsimodel.LsiModel
    # Running and Trainign LSI model on the document term matrix.
    if TF_IDF:
        print("use tf-idf corpus to train model...")
        lsimodel = Lsi(corpus_tfidf, num_topics=NUM_TOPICS, id2word = dictionary, onepass = False)
    else:
        print("use normal corpus to train model...")
        lsimodel = Lsi(corpus, num_topics=NUM_TOPICS, id2word = dictionary, onepass = False)
    lsimodel.save(LSI_PATH)
else:
    lsimodel = gensim.models.LsiModel.load(LSI_PATH)
    print("lsi model loaded...")


if not os.path.exists(LSI_INDEX):
    if TF_IDF:
        index = similarities.MatrixSimilarity(lsimodel[corpus_tfidf], num_features=NUM_TOPICS)
    else:
        index = similarities.MatrixSimilarity(lsimodel[corpus], num_features=NUM_TOPICS)
    index.save(LSI_INDEX)
else:
    index = similarities.MatrixSimilarity.load(LSI_INDEX)


def find_most_similar_subreddit_lsi(name):
    """
    Given a subreddit name, use that document vector to find the closest one. 
    """
    if name in subreddits:
        sub_id = subreddits.index(name)
        sub_tfidf = corpus_tfidf[sub_id]
        sims = index[lsimodel[sub_tfidf]]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])   
        res = map(lambda x: (subreddits[x[0]], x[1]), sims[:10])
        # print res
    else:
        print("subreddit not found...")

def find_most_similar_combined_subreddit_lsi(name1, name2, add = True):
    if  name1 in subreddits and name2 in subreddits:
        sub_tfidf1 = corpus_tfidf[subreddits.index(name1)]
        sub_tfidf2 = corpus_tfidf[subreddits.index(name2)]
        sub_vec1 = lsimodel[sub_tfidf1]
        sub_vec2 = lsimodel[sub_tfidf2]
        if add:
            comb_vec = []
            for vec1, vec2 in zip(sub_vec1, sub_vec2):
                comb_vec.append((vec1[0], vec1[1] + vec2[1]))
        else:
            comb_vec = []
            for vec1, vec2 in zip(sub_vec1, sub_vec2):
                comb_vec.append((vec1[0], vec1[1] - vec2[1]))
        # print comb_vec
        sims = index[comb_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])   
        res = map(lambda x: (subreddits[x[0]], x[1]), sims[:10])
        return res
    else:
        print("at least one of the subreddit not found...")


def find_most_similar_algebra_subreddit_lsi(male, female, male_like):
    """
    Investigate if there are phenomenon like male - female = male_like - female_like. 
    """
    if  male in subreddits and female in subreddits and male_like in subreddits:
        sub_tfidf1 = corpus_tfidf[subreddits.index(male)]
        sub_tfidf2 = corpus_tfidf[subreddits.index(female)]
        sub_tfidf3 = corpus_tfidf[subreddits.index(male_like)]
        sub_vec1 = lsimodel[sub_tfidf1]
        sub_vec2 = lsimodel[sub_tfidf2]
        sub_vec3 = lsimodel[sub_tfidf3]
        comb_vec = []
        for vec1, vec2, vec3 in zip(sub_vec1, sub_vec2, sub_vec3):
            comb_vec.append((vec1[0], vec3[1] - vec1[1] + vec2[1]))
        # print comb_vec
        sims = index[comb_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])   
        res = map(lambda x: (subreddits[x[0]], x[1]), sims[:10])
        return res
    else:
        print("at least one of the subreddit not found...")



# import construction from module.
from construct_vec_from_overlap import *

names, name2vec, indexing = construct_mapping_from_overlap()

def test_binary(command1, command2, if_add):
    sign = " + " if if_add else " - "
    print("{0}{1}{2}:".format(command1, sign, command2))
    lsi_res = find_most_similar_combined_subreddit_lsi(command1, command2, add = if_add)
    print("result by LSI: ", lsi_res)
    overlap_res = find_most_similar_combined_subreddit_overlap(names, name2vec, indexing, command1, command2, add = if_add)
    print("result by finding overlap commenters: ", overlap_res)

def test_trinary(command1, command2, command3):
    print("{0} - {1} = {2} - ?:".format(command1,command2, command3))
    lsi_res = find_most_similar_algebra_subreddit_lsi(command1, command2, command3)
    print("result by LSI: ", lsi_res)
    overlap_res = find_most_similar_algebra_subreddit_overlap(names, name2vec, indexing, command1, command2, command3)
    print("result by finding overlap commenters: ", overlap_res)



command1 = 'AskMen'
command2 = 'AskWomen'
command3 = 'The_Donald'
if_add = False

# test_binary(command1, command2, if_add)
test_trinary(command1, command2, command3)


