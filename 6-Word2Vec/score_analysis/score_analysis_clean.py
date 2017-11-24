from __future__ import division
import pandas as pd
import os.path
import math

VERSION_PATH = './models/no_tfidf_topic_100_31G_data'
NEW_AUTHOR_CSV = os.path.join(VERSION_PATH, 'score_analysis_clean.csv')

def save_new_csv_file():
    
    AUTHOR_CSV = os.path.join(VERSION_PATH, 'score_analysis.csv')
    f=pd.read_csv(AUTHOR_CSV)
    new_f = f.drop('involvement_sorted', 1)
    new_f.to_csv(NEW_AUTHOR_CSV, index=False)

def calculate_diff():
    f = pd.read_csv(NEW_AUTHOR_CSV)
    lda_scores = f['mapped_score'].tolist()
    overlap_scores = f['mapped_score_by_overlap'].tolist()
    diff = [abs(x - y) for x, y in zip(lda_scores, overlap_scores)]
    print diff[0]
    aver = sum(diff) / len(diff)
    print aver

# calculate_diff()
save_new_csv_file()