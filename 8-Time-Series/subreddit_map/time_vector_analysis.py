"""
Final goals:

if the G/S scores will changes over time. 

draw plots on slopes of time vectors to G/S score. Hypothesis: if high score will lead to higher increase? or flat?

Procedure:

- Generate time vector from three dataset on shared subreddits.
- Draw plots.

contains fields:
['involvements', 'all_scores_overlap', 'name', 'elite_scores_overlap']

"""
import os.path
import pickle
from collections import defaultdict

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

SHARED_REDDITS = os.path.join('./models', 'shared_reddits.pkl')

subreddit_name_lst = map(lambda x: x.iterkeys(), [reddit_stats_2013, reddit_stats_2014, reddit_stats_2015])

shared_name_lst = list(reduce(set.intersection, [set(year) for year in subreddit_name_lst ]))

shared_reddits = defaultdict(dict)
for reddit_name in shared_name_lst:
    involvements_time_vec = []
    allscore_time_vec = []
    elitescore_time_vec = []
    for data in [reddit_stats_2013, reddit_stats_2014, reddit_stats_2015]:
        involvements_time_vec.append(len(data[reddit_name]['involvements']))
        allscore_time_vec.append(data[reddit_name]['all_scores_overlap'])
        elitescore_time_vec.append(data[reddit_name]['elite_scores_overlap'])
    shared_reddits[reddit_name]['involvement_vec'] = involvements_time_vec
    shared_reddits[reddit_name]['all_score_vec'] = allscore_time_vec
    shared_reddits[reddit_name]['elite_score_vec'] = elitescore_time_vec

pickle.dump(shared_reddits, open(SHARED_REDDITS, 'wb'))

