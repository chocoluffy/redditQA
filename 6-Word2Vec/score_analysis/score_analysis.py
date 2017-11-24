import pickle
import os.path
import csv
from collections import defaultdict
from operator import itemgetter

VERSION_PATH = './models/no_tfidf_topic_100_31G_data'
REDDIT_ALL = os.path.join(VERSION_PATH, 'reddit_all.pkl')
AUTHOR_STATS = os.path.join(VERSION_PATH, 'complete_author_stats.pkl') # each author's statistics. 
SCORE_ANALYSIS = os.path.join(VERSION_PATH, 'score_analysis.csv')

"""
Global Configuration
"""
KEYWORD = 'entropy' # 'lda'; 'overlap'; 'entropy'
ELITE_PERCENTAGE = 0.1 # meaning pick the top 10% authors as elite users.

common_score = 'scores_by_' + KEYWORD
elite_score = 'elite_scores_' + KEYWORD


"""
contains field:
    - scores_by_lda: list of int.
    - scores_by_overlap
    - scores_by_entropy
    - elite_scores_lda: int.
    - elite_scores_overlap
    - elite_scores_entropy
"""
reddit = pickle.load(open(REDDIT_ALL, 'rb'))
print("reddit stats loaded...")

"""
contains field:
    - contributions_by_count
"""
author_stats = pickle.load(open(AUTHOR_STATS, 'rb'))
print("author stats loaded...")

"""
Construct dictionary
    - reddit name
    - relative value: elite score - common score
    - percentage of the elite's most active subreddit equals the same one.
    - involvement (most active author involves 100~500 comments in total, least elite involves )
"""
analysis = defaultdict(dict)
for reddit_name, reddit_obj in reddit.iteritems():
    if len(reddit_obj['involvements']) > 500: # only pick active subreddits.
        analysis[reddit_name]['name'] = reddit_name
        common_people_score = sum(reddit_obj[common_score]) / len(reddit_obj[common_score])
        analysis[reddit_name]['relative_score'] = reddit_obj[elite_score] - common_people_score # most positive means most specialist elites dominated.
        involvement_sorted = sorted(reddit_obj['involvements'], key=lambda tup: tup[2], reverse=True) # sorted by total comments counts.
        analysis[reddit_name]['involvement_sorted'] = involvement_sorted

        total = len(involvement_sorted) * ELITE_PERCENTAGE
        counter = 0
        truth_teller = []
        while counter < total:
            author_name = involvement_sorted[counter][0]
            contributions_sorted = sorted(author_stats[author_name]['contributions_by_count'].iteritems(), key=itemgetter(1), reverse=True)
            if contributions_sorted[0][0] == reddit_name:
                truth_teller.append(1)
            counter += 1

        percentage = len(truth_teller) / round(total)
        analysis[reddit_name]['percentage'] = percentage

"""
Generate csv file.
"""

# print reddit
csv_file_path = SCORE_ANALYSIS
csv_file = open(csv_file_path, 'wb')
writer = csv.writer(csv_file, dialect='excel')

headers = ['name', 'relative_score', 'involvement_sorted', 'percentage']
writer.writerow(headers)

for name, obj in analysis.items():
    # print key, value
    line = []
    for field in headers:
        line.append(obj[field])
    writer.writerow(line)
    
csv_file.close()



