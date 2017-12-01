"""
Run `python score_analysis/draw_score_distribution.py` at root folder.
"""
from __future__ import division
import pickle
import os.path
import csv
from collections import defaultdict
import math

VERSION_PATH = './models/no_tfidf_topic_100_8G_data'
REDDIT_ALL = os.path.join(VERSION_PATH, '31G_reddit_all.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, '31G_complete_author_stats.pkl') # each author's statistics. 
TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments_with_author.pkl')
NEW_TOP_COMMENTS = os.path.join(VERSION_PATH, '8G_top010subreddit_top2kcomments_with_author_and_score.pkl')
TOP_SUCCESSFUL_AUTHOR_SCORE_ANALYSIS = os.path.join(VERSION_PATH, '8G_most_successful_author_score_analysis.csv')
REDDIT_SCORE_TO_COMMENT = os.path.join(VERSION_PATH, '8G_suddreddit_score_to_comments.pkl')

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

headers = ['name', 'comments_count', 'valid_comment_count']
headers.extend(map(lambda x: str(x), TOP_K_SUCCESSFUL_AUTHOR))
writer.writerow(headers)


if not os.path.exists(REDDIT_SCORE_TO_COMMENT):
    reddit_score_to_comment_count = defaultdict(dict)
    for reddit_name, obj in new_top_comments.items():
        line = []
        for field in headers:
            if field == 'name':
                line.append(reddit_name)
            elif field == 'comments_count':
                line.append(obj['length'])
                reddit_score_to_comment_count[reddit_name]['comments_count'] = obj['length']
            elif field == 'valid_comment_count':
                line.append(len(obj['top_comments']))
                reddit_score_to_comment_count[reddit_name]['valid_comment_count'] = len(obj['top_comments'])
            else: # a percentage
                ratio = float(field)
                id = math.ceil(len(obj['top_comments']) * ratio)
                counter = 0
                score_lst = []
                while counter < id:
                    score_lst.append(obj['top_comments'][counter][2]) # add the mapped_score_overlap
                    counter += 1
                if len(score_lst) > 0:
                    score_average = sum(score_lst) / len(score_lst)
                else:
                    score_average = []
                line.append(score_average)
                reddit_score_to_comment_count[reddit_name][field] = score_average
        writer.writerow(line)
        
    csv_file.close()
    pickle.dump(reddit_score_to_comment_count, open(REDDIT_SCORE_TO_COMMENT, 'wb'))
else: 
    reddit_score_to_comment_count = pickle.load(open(REDDIT_SCORE_TO_COMMENT, 'rb'))

        

"""
Make plot.
"""
import numpy as np 
import matplotlib as mpl 

## agg backend is used to create plot as a .png file
mpl.use('agg')

import matplotlib.pyplot as plt 

def init_list_of_objects(size):
    list_of_objects = list()
    for i in range(0,size):
        list_of_objects.append( list() ) #different object reference each time
    return list_of_objects


def plot(reddit_score_to_comment_count, adjust = False):

    data_collections = init_list_of_objects(20) # each 5 point a bucket: such as 50~55

    # pprint(reddit)
    for name, obj in reddit_score_to_comment_count.iteritems():
        if obj['1'] and obj['0.1']:
            bucket_id = round(obj['1'] / 5)
            data_collections[int(bucket_id)].append(obj['0.1'])
            # print data_collections

    # Create a figure instance
    fig = plt.figure(1, figsize=(9, 6))

    # Create an axes instance
    ax = fig.add_subplot(111)

    ax.set_xticklabels(map(lambda x: str(x), range(0, 100, 5)))

    # Create the boxplot
    bp = ax.boxplot(data_collections)

    # Save the figure
    fig.savefig('./results/most_successful_author_score_to_subreddit_score_boxplot.png', bbox_inches='tight')

plot(reddit_score_to_comment_count, adjust = True)