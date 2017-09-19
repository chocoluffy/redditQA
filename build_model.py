import json
import pandas
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.cluster import KMeans
import sklearn.metrics.pairwise as smp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pickle
from collections import defaultdict
from sklearn.externals import joblib
from pymongo import MongoClient

num_comments = 10e6
chunksize= 1e6

stopset = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r'\w+')

# Use pymongo to achieve same effect as below codes. 
con = MongoClient('localhost', 27017)
db = con.test
pipe = [
    {'$group': {'_id': '$subreddit', 'comments': {'$addToSet': '$body'}}},
    {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
    {'$match': {"commentsCount": {'$gt': 100 }}},
    { '$project': { '_id': 1, 'hundredsComments': { '$slice': [ "$comments", 100 ] } } }
]

sub_data = defaultdict(dict)
counter = 0
for document in db.docs_large.aggregate(pipeline = pipe, allowDiskUse = True):

    def clean_and_stem(doc):
        # Drop digits
        s = re.sub("\d+", "", doc)
        s = s.replace("_", " ")

        # Tokenize and stem words
        s = [stemmer.stem(w.lower()) for w in tokenizer.tokenize(s) if w.lower() not in stopset]

        return " ".join(s)

    # print document
    # print document.keys()
    counter += 1
    print "Processing #%d subreddit"%(counter)
    print "Cleaning and stemming comments..."
    document['hundredsComments'] = map(lambda x: clean_and_stem(x), document['hundredsComments'])
    print "Done stemming."

    docset = " ".join(document['hundredsComments'])
    sub_data[document['_id']]['docset'] = docset
    sub_data[document['_id']]['length'] = len(document['hundredsComments'])

pickle.dump(sub_data, open("models/sub_data.pkl", 'wb'))

print "Building model..."

print "Tfidf transform..."
tfi = TfidfVectorizer(ngram_range=(1,1), lowercase=True, min_df= 2./len(sub_data) )
X = tfi.fit_transform([sub['docset'] for sub in sub_data.values()])

joblib.dump(tfi, "models/tfi.pkl")

print "Calculating Truncated SVD..."
lsa = TruncatedSVD(n_components=1000, n_iter=10)
X_reduced = lsa.fit_transform(X)
print "Finished SVD"

joblib.dump(lsa, "models/lsa.pkl")

sub_comps = {sub: {"components":X_reduced[i], "length":sub_data[sub]['length']} for i, sub in enumerate(sub_data.keys())}

pickle.dump(sub_comps, open("models/sub_comps2.pkl", 'wb'))

print "Done!"
print "Number of subreddits analyzed:" , len(sub_data)

