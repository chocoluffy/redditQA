import pickle
import praw
from collections import defaultdict
import sklearn.metrics.pairwise as smp
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
import re
from gensim.models.lsimodel import LsiModel
from gensim import corpora, models, similarities
from gensim.matutils import Sparse2Corpus
from sklearn.externals import joblib

stopset = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")
tokenizer = RegexpTokenizer(r'\w+')

def clean_and_stem(doc):
    # Drop digits
    s = re.sub("\d+", "", doc)
    s = s.replace("_", " ")
  
    # Tokenize words
    s = [w.lower() for w in tokenizer.tokenize(s) if w.lower() not in stopset]
    
    # Stem all words
    s = [stemmer.stem(w) for w in s]

    return " ".join(s)


sub_components = pickle.load(open("models/sub_comps2.pkl", 'rb'))
tfi = joblib.load("models/tfi.pkl")
lsa = joblib.load("models/lsa.pkl")

# r = praw.Reddit(user_agent="subreddit recommender by Nihilist_Fuck")


front_page_subs = set(['announcements',
 'Art',
 'AskReddit',
 'askscience',
 'aww',
 'blog',
 'books',
 'bestof',
 'creepy',
 'dataisbeautiful',
 'DIY',
 'Documentaries',
 'EarthPorn',
 'explainlikeimfive',
 'food',
 'funny',
 'Futurology',
 'gadgets',
 'gaming',
 'GetMotivated',
 'gifs',
 'history',
 'IAmA',
 'InternetIsBeautiful',
 'Jokes',
 'LifeProTips',
 'listentothis',
 'mildlyinteresting',
 'movies',
 'Music',
 'news',
 'nosleep',
 'nottheonion',
 'OldSchoolCool',
 'personalfinance',
 'philosophy',
 'photoshopbattles',
 'pics',
 'science',
 'Showerthoughts',
 'space',
 'sports',
 'television',
 'tifu',
 'todayilearned',
 'TwoXChromosomes',
 'UpliftingNews',
 'videos',
 'worldnews',
 'WritingPrompts',
 'india'  ])

rarer_subs = {key:val for (key, val) in sub_components.items() if key not in front_page_subs}


def cosine_matches(components, other_subs, n_matches=5):
    other_subs, data = other_subs.keys(), other_subs.values()
    other_components = [comp['components'] for comp in data]
    cos_sim = smp.cosine_similarity(components, other_components)[0]
    top_ind = cos_sim.argsort()[-1:-n_matches-1:-1]
        
    return [other_subs[i] for i in top_ind], cos_sim[top_ind]

def euc_matches(components, other_subs, n_matches=5):
    other_subs, data = other_subs.keys(), other_subs.values()
    other_components = [comp['components'] for comp in data]
    dist = smp.euclidean_distances(components, other_components)[0]
    
    top_ind = dist.argsort()[:n_matches]
        
    return [other_subs[i] for i in top_ind], dist[top_ind]

def comments_to_vect(comments, tfi, lsa):
    comments = " ".join([comment["body"] for comment in comments])
    comments = clean_and_stem(comments)
    X = tfi.transform([comments])
    return lsa.transform(X)

    
def generate_user_suggestions(username):
    user = r.get_redditor(username)
    subreddits = defaultdict(int)
    
    comments = []
    for comment in user.get_comments():
        comments.append(comment)
        
        if comment.subreddit.display_name in sub_components:
            subreddits[comment.subreddit.display_name] += 1
      
    used = []
    recs_per_sub = 1 + 20 / len(subreddits)
    suggestions = []

    top_subs = sorted(subreddits.items(), key=lambda x: x[1], reverse=True)
    top_subs = [sub[0] for sub in top_subs]
    for sub in top_subs[:6]:
        try:
            components = sub_components[sub]['components']

            sub_matches = set(cosine_matches(components, rarer_subs, recs_per_sub)[0] + 
                         euc_matches(components, rarer_subs, recs_per_sub)[0])
            
            
            # Don't recommend subs the user already uses
            for item in subreddits.keys():
                sub_matches.discard(item)
           
            # Don't recommend subs already recommended
            for s, recs in suggestions:
                for rec in recs:
                    sub_matches.discard(rec)
            print 
       
            suggestions.append((sub, sub_matches))  


        except KeyError:
            print sub + " not in db"


    vect = comments_to_vect(comments, tfi, lsa)
    cosine_res = cosine_matches(vect, rarer_subs, 8)
    euc_res = euc_matches(vect, rarer_subs, 8)
    print cosine_res, euc_res
    alternate_suggestions = set(cosine_res[0] + euc_matches[0])
            
            
    return suggestions, alternate_suggestions

def playground():
    
    comments = []
    print "Suggest you sub reddit given your words. "
    while True:
        com = raw_input('Enter your comment: \n')
        comments.append({"body": com})
        vect = comments_to_vect(comments, tfi, lsa)
        print "%d comments yields the following suggestions."%(len(comments))
        cosine_res = cosine_matches(vect, rarer_subs, 8)
        euc_res = euc_matches(vect, rarer_subs, 8)
        # print cosine_res, euc_res
        # alternate_suggestions = set(cosine_res[0] euc_matches[0])
            
        # print alternate_suggestions
        print cosine_res[0]
        print euc_res[0]
        print 



playground()