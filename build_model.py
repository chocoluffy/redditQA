import json
from sqlalchemy import create_engine
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

# print "loading %d reddit comments with chunksize %d"%(num_comments, chunksize)

# def connect_db():
#     cred = json.load(open("db_cred.json"))
#     engine = create_engine('postgresql://' + cred["username"] + ":" + 
#                            cred["password"] + "@" + cred["db_url"] + "/" 
#                            + cred["database"])
#     return engine

# con = connect_db()

# print "loading comments into data frame from sql database..."


# df_iterator = pandas.read_sql_query("select * from comments limit %d;"%num_comments, con, chunksize=chunksize)


# sub_data = defaultdict(dict)
# for df in df_iterator:
#     print "loading new chunk of data from database..."
    
#     # Drop bodyless comments and convert subreddit names to strings
#     df = df.dropna(subset=['body', 'subreddit'])
#     df.loc[:, "subreddit"] = df.subreddit.astype(unicode)
#     df.loc[:, "link_id"] = df.link_id.astype(unicode)

#     def is_id(s):
#         if re.match("^t._", s):
#             return True
#         else:
#             return False

#     def is_nan(s):
#         return s.lower()=="nan"

#     # Clean the data. Sometimes subreddit and link_id are backwards; fix this
#     mask = df.subreddit.apply(lambda s: is_id(s))
#     df.loc[:, 'subreddit'][mask] = df['link_id'][mask]

#     # Drop subreddits with the name "nan"
#     isnan = df.subreddit.apply(is_nan)
#     df = df[~isnan]

#     # Just keep subs with more than 100 comments (per million comments... .1% of all comments)
#     #counts = df.subreddit.value_counts()
#     #counts = counts[counts > 50]
#     #df = df.set_index("subreddit").loc[counts.keys()].reset_index()


#     def clean_and_stem(doc):
#         # Drop digits
#         s = re.sub("\d+", "", doc)
#         s = s.replace("_", " ")

#         # Tokenize and stem words
#         s = [stemmer.stem(w.lower()) for w in tokenizer.tokenize(s) if w.lower() not in stopset]

#         return " ".join(s)

#     print "Cleaning and stemming comments..."
#     df.body = df.body.apply(clean_and_stem)
#     print "Done stemming."
    
#     print "Grouping by subreddits..."
#     for sub, posts in df.groupby("subreddit").body:
#         docset = " ".join(posts)
        
#         if sub in sub_data:
#             sub_data[sub]['docset'] += docset
#             sub_data[sub]['length'] += len(posts)
#         else:
#             sub_data[sub]['docset'] = docset
#             sub_data[sub]['length'] = len(posts)
    
  
# Just keep subs with more than 100 comments (per million comments... .1% of all comments)
# sub_data = {sub:sub_data[sub] for sub in sub_data.keys() if sub_data[sub]['length'] > 100}

pickle.dump(sub_data, open("models/sub_data.pkl", 'wb'))


#sub_data = pickle.load(open("models/sub_data.pkl", 'rb'))

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

