"""
Final goals:

if the G/S scores will changes over time. 

draw plots on slopes of time vectors to G/S score. Hypothesis: if high score will lead to higher increase? or flat?

Procedure:

- Generate time vector from three dataset on shared subreddits.
- Draw plots.
"""
import os.path
import pickle

VERSION_PATH_2013 = './models/201301'
SUBREDDIT_STATS_2013 = os.path.join(VERSION_PATH_2013, 'reddit_stats.pkl')
reddit_stats_2013 = pickle.load(open(SUBREDDIT_STATS_2013, 'rb'))
print "loaded reddit stats at 201301"

VERSION_PATH_2014 = './models/201401'
SUBREDDIT_STATS_2014 = os.path.join(VERSION_PATH_2014, 'reddit_stats.pkl')
reddit_stats_2014 = pickle.load(open(SUBREDDIT_STATS_2014, 'rb'))
print "loaded reddit stats at 201401"

VERSION_PATH_2015 = './models/201501'
SUBREDDIT_STATS_2015 = os.path.join(VERSION_PATH_2015, 'reddit_stats.pkl')
reddit_stats_2015 = pickle.load(open(SUBREDDIT_STATS_2015, 'rb'))
print "loaded reddit stats at 201501"




