import pickle
import os.path

VERSION_PATH = './models/no_tfidf_topic_100_31G_data'
REDDIT_ALL = os.path.join(VERSION_PATH, 'reddit_all.pkl')

KEYWORD = 'entropy' # 'lda'; 'overlap'; 'entropy'

common_score = 'scores_by_' + KEYWORD
elite_score = 'elite_scores_' + KEYWORD

"""
contains field:
    - scores_by_lda
    - scores_by_overlap
    - scores_by_entropy
    - elite_scores_lda
    - elite_scores_overlap
    - elite_scores_entropy
"""
reddit = pickle.load(open(REDDIT_ALL, 'rb'))
print("reddit stats loaded...")


"""
Examine involvement scale.
"""
involvements = []
for name, obj in reddit.iteritems():
    if len(obj['involvements']) > 500:
        # print(obj['involvements'])
        lst = sorted(obj['involvements'], key=lambda tup: tup[2], reverse=True)
        print(lst[0], lst[-1])


"""
Make plot.
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
from adjustText import adjust_text

def plot(reddit_data, adjust = False):
    """
    x: average generalist/specialist score.
    y: average elite's generalist/specialist score.
    radius: total authors involved.
    """
    labels = []
    x = []
    y = []
    r = []


    # pprint(reddit)
    for name, obj in reddit_data.iteritems():
        if len(obj['involvements']) > 500: # only pick active subreddits.
            labels.append(name)
            x.append(sum(obj[common_score]) / len(obj[common_score]))
            y.append(obj[elite_score])
            r.append(len(obj['involvements']))
    
    colors = cm.rainbow(np.linspace(0, 1, len(labels)))
                   
    fig = plt.figure(figsize=(16, 16)) 
    axes = plt.gca()
    axes.set_xlim([1,100])
    axes.set_ylim([1,100])
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('average G/S score')
    ax.set_ylabel('average elite G/S score')
    ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
    plt.title("common VS elites G/S score")

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
            sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 0.1), linewidths=2, edgecolor='w')
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

plot(reddit, adjust = True)
