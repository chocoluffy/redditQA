"""
Run `python score_analysis/draw_score_distribution.py` at root folder.
"""
from __future__ import division
import pickle
import os.path
import csv
from collections import defaultdict

VERSION_PATH = './models/no_tfidf_topic_100_8G_data'
REDDIT_ALL = os.path.join(VERSION_PATH, '31G_reddit_all.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, '31G_complete_author_stats.pkl') # each author's statistics. 
TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments_with_author.pkl')
NEW_TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments_with_author_and_score.pkl')
TOP_SUCCESSFUL_AUTHOR_SCORE_ANALYSIS = os.path.join(VERSION_PATH, '8G_most_successful_author_score_analysis.csv')

TOP_K_SUCCESSFUL_AUTHOR = [0.01, 0.05, 0.1, 0.2, 0.5, 1] # check score from those top successful authors from each subreddit.
KEYWORD = 'lda' # 'lda'; 'overlap'; 'entropy'

common_score = 'scores_by_' + KEYWORD
elite_score = 'elite_scores_' + KEYWORD

if not os.path.exists(NEW_TOP_COMMENTS):
    """
    contains field:
        - scores_by_lda
        - scores_by_overlap
        - scores_by_entropy
        - elite_scores_lda
        - elite_scores_overlap
        - elite_scores_entropy
    """
    # reddit = pickle.load(open(REDDIT_ALL, 'rb'))
    # print("reddit stats loaded...")

    """
    Each author's information lookup, contains field:
        - mapped_score
        - mapped_score_by_overlap
        - mapped_score_by_entropy
        - contributions_by_count
        - contributions (by total votes)
    """
    author_stats = pickle.load(open(AUTHOR_STATS, 'rb'))
    print("author stats loaded...")

    """
    contains field:
        - top_comments: [{ups: ; author: }, ...]
        - length
    """
    top_comments = pickle.load(open(TOP_COMMENTS, 'rb'))
    print("comment data loaded...")


    new_top_comments = defaultdict(dict)
    for reddit_name in top_comments:
        comments = top_comments[reddit_name]['top_comments']
        comments = filter(lambda x: x['author'] in author_stats, comments)
        comments = map(lambda x: (x['ups'], x['author'], author_stats[x['author']]['mapped_score_by_overlap']), comments)
        new_top_comments[reddit_name]['top_comments'] = comments
        new_top_comments[reddit_name]['length'] = top_comments[reddit_name]['length']

    pickle.dump(new_top_comments, open(NEW_TOP_COMMENTS, 'wb'))
else:
    new_top_comments = pickle.load(open(NEW_TOP_COMMENTS, 'rb'))

"""
Generate csv file.
"""

# print reddit
csv_file_path = TOP_SUCCESSFUL_AUTHOR_SCORE_ANALYSIS
csv_file = open(csv_file_path, 'wb')
writer = csv.writer(csv_file, dialect='excel')

headers = ['name', 'comments_count'].extend(map(lambda x: str(x), TOP_K_SUCCESSFUL_AUTHOR))
writer.writerow(headers)

for reddit_name, obj in new_top_comments.items():
    line = []
    for field in headers:
        if field == 'name':
            line.append(reddit_name)
        elif field == 'comments_count':
            line.append(obj['length'])
        else: # a percentage
            ratio = float(field)
            id = round(len(obj['top_comments']) * ratio)
            counter = 0
            score_lst = []
            while counter < id:
                score_lst.append(obj['top_comments'][counter])
                counter += 1
            score_average = sum(score_lst) / len(score_lst)
            line.append(score_average)

    writer.writerow(line)
    
csv_file.close()




        


# """
# Make plot.
# """
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import numpy as np
# import math
# from adjustText import adjust_text

# def plot(reddit_data, adjust = False):
#     """
#     x: average generalist/specialist score.
#     y: average elite's generalist/specialist score.
#     radius: total authors involved.
#     """
#     labels = []
#     x = []
#     y = []
#     r = []


#     # pprint(reddit)
#     for name, obj in reddit_data.iteritems():
#         if len(obj['involvements']) > 500: # only pick active subreddits.
#             labels.append(name)
#             x.append(sum(obj[common_score]) / len(obj[common_score]))
#             y.append(obj[elite_score])
#             r.append(len(obj['involvements']))
    
#     colors = cm.rainbow(np.linspace(0, 1, len(labels)))
                
#     fig = plt.figure(figsize=(16, 16)) 
#     axes = plt.gca()
#     axes.set_xlim([1,100])
#     axes.set_ylim([1,100])
#     ax = fig.add_subplot(111)
#     fig.subplots_adjust(top=0.85)
#     ax.set_xlabel('average G/S score')
#     ax.set_ylabel('average elite G/S score')
#     ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
#     plt.title("common VS elites G/S score")

#     # to dynamic adjust texts labels.
#     texts = []
#     annotate_x = []
#     annotate_y = []
#     for xx, yy, ll in zip(x, y, labels):
#         if abs(yy - xx) > 10:
#             texts.append(ax.text(xx, yy, ll))
#             annotate_x.append(xx)
#             annotate_y.append(yy)

#     if adjust:
#         for i in range(len(x)):
#             sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 0.1), linewidths=2, edgecolor='w')
#             sct.set_alpha(0.75)
#         adjust_text(texts, annotate_x, annotate_y, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))
#     else:
#         for i in range(len(x)):
#             sct = plt.scatter(x[i],y[i], color=colors[i], s=(float(r[i]) * 0.1), linewidths=2, edgecolor='w')
#             sct.set_alpha(0.75)
#             if abs(y[i] - x[i]) > 25:
#                 plt.annotate(labels[i],
#                             xy=(x[i], y[i]),
#                             xytext=(5, 2),
#                             textcoords='offset points',
#                             ha='right',
#                             va='bottom')
#     plt.show()

# plot(reddit, adjust = True)