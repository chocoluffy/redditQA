import os.path
from author_csv import *

VERSION_PATH = './models/no_tfidf_topic_100_31G_data'
AUTHOR_CSV = os.path.join(VERSION_PATH, 'each_author_topic_comment.csv')

author_stats_large = return_author_stats(VERSION_PATH)
write_dict_data_to_csv_file(AUTHOR_CSV, author_stats_large):