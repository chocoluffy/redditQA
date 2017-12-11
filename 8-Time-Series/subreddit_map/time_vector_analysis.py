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

SHARED_REDDITS = os.path.join('./models', 'shared_reddits.pkl')

if not os.path.exists(SHARED_REDDITS):
    """
    Create shared reddit on time-series vectors.
    """
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
else:
    shared_reddits = pickle.load(open(SHARED_REDDITS, 'rb'))

"""
shared_reddits['xx'] = {
    'all_score_vec': [62.954332123661288, 64.182131043307209, 67.457798134450996],
    'elite_score_vec': [63.942701321611672,66.511118679587668,68.32487556219381],
    'involvement_vec': [1107, 2339, 2572]}

flat_lst[0] = (u'AskReddit',
 {'all_score_vec': [67.15534132579343, 65.16583358182379, 67.747326336563731],
  'elite_score_vec': [74.057390274643637,
   72.203303092364877,
   74.608426740685303],
  'involvement_vec': [207352, 236393, 271352]})
"""
flat_lst = [(name, shared_reddits[name]) for name in shared_reddits]
flat_lst = sorted(flat_lst, key=lambda x: min(x[1]['involvement_vec']), reverse=True)

TOP_PERCENTAGE = 0.01
slice_id = int(round(len(flat_lst) * TOP_PERCENTAGE))
top_reddit_lst = flat_lst[:slice_id]


"""
Make plot:

- G/S scores slope - average G/S score: if high specialized community will becomes more specialized?
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from adjustText import adjust_text

def plot_trend(top_reddit_lst, adjust = False):
    """
    x: average generalist/specialist score.
    y: G/S scores slop
    radius: min involvements
    """
    labels = []
    x = []
    y = []
    r = []


    # pprint(reddit)
    for name, obj in top_reddit_lst:
        labels.append(name)
        x.append(sum(obj['all_score_vec']) / len(obj['all_score_vec']))

        # run linear regression to calculate slope of lst of int.
        xx = np.arange(0,len(obj['all_score_vec']))
        yy = np.array(obj['all_score_vec'])
        z = np.polyfit(xx,yy,1)

        y.append(z[0]) 
        r.append(min(obj['involvement_vec']))
    
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
                   
    fig = plt.figure(figsize=(16, 16)) 
    axes = plt.gca()
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('average G/S score')
    ax.set_ylabel('G/S time vector linear slope')
    plt.title("trend analysis")

    # to dynamic adjust texts labels.
    texts = []
    annotate_x = []
    annotate_y = []
    for xx, yy, ll in zip(x, y, labels):
        if abs(yy - xx) > 10:
            texts.append(ax.text(xx, yy, ll))
            annotate_x.append(xx)
            annotate_y.append(yy)

    if adjust:
        for i in range(len(x)):
            sct = plt.scatter(x[i],y[i], color=colors[i], s=(math.log1p(float(r[i]))*10), linewidths=2, edgecolor='w')
            sct.set_alpha(0.75)
        adjust_text(texts, annotate_x, annotate_y, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))
    else:
        for i in range(len(x)):
            sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 0.1), linewidths=2, edgecolor='w')
            sct.set_alpha(0.75)
            if abs(y[i] - x[i]) > 25:
                plt.annotate(labels[i],
                            xy=(x[i], y[i]),
                            xytext=(5, 2),
                            textcoords='offset points',
                            ha='right',
                            va='bottom')
    plt.show()

def plot_elite(top_reddit_lst, adjust = False):
    """
    x: average generalist/specialist score.
    y: average elite generalist/specialist score.
    radius: min involvements
    """
    labels = []
    x = []
    y = []
    r = []


    # pprint(reddit)
    for name, obj in top_reddit_lst:
        labels.append(name)
        x.append(sum(obj['all_score_vec']) / len(obj['all_score_vec']))
        y.append(sum(obj['elite_score_vec']) / len(obj['elite_score_vec']))
        r.append(min(obj['involvement_vec']))
    
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
                   
    fig = plt.figure(figsize=(16, 16)) 
    axes = plt.gca()
    axes.set_xlim([50,80])
    axes.set_ylim([50,80])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
    ax.set_xlabel('average G/S score')
    ax.set_ylabel('average elite G/S score')
    plt.title("elite comparison")

    # to dynamic adjust texts labels.
    texts = []
    annotate_x = []
    annotate_y = []
    for xx, yy, ll in zip(x, y, labels):
        texts.append(ax.text(xx, yy, ll))
        annotate_x.append(xx)
        annotate_y.append(yy)

    if adjust:
        for i in range(len(x)):
            sct = plt.scatter(x[i],y[i], color=colors[i], s=(math.log1p(float(r[i]))*10), linewidths=2, edgecolor='w')
            sct.set_alpha(0.75)
        adjust_text(texts, annotate_x, annotate_y, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))
    else:
        for i in range(len(x)):
            sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 0.1), linewidths=2, edgecolor='w')
            sct.set_alpha(0.75)
            if abs(y[i] - x[i]) > 25:
                plt.annotate(labels[i],
                            xy=(x[i], y[i]),
                            xytext=(5, 2),
                            textcoords='offset points',
                            ha='right',
                            va='bottom')
    plt.show()

# plot_trend(top_reddit_lst, adjust = True)
plot_elite(top_reddit_lst, adjust = True)
  
