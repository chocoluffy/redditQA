from __future__ import division # to force division be float.
import csv
import pickle
from operator import itemgetter
import gensim
from gensim import corpora
from collections import defaultdict
from scipy.interpolate import interp1d
from scipy.stats import entropy
import os.path
import itertools
import math



# import construction from module.
from construct_vec_from_overlap import *



def return_author_stats(path = './models/no_tfidf_topic_100_8G_data'):
    """
    Finally return author_stats data with additional score_by_overlap and mapped_score_by_overlap.
    """

    # Model path.
    # VERSION_PATH = './models/lsi_tfidf_topic_100'
    VERSION_PATH = path

    AUTHOR_COMMENT_RAW = os.path.join(VERSION_PATH, 'each_author_topic_comments_with_count.pkl')
    LDA_MODEL = os.path.join(VERSION_PATH, 'model.lda')

    author_stats = pickle.load(open(AUTHOR_COMMENT_RAW, 'rb'))
    ldamodel = gensim.models.ldamodel.LdaModel.load(LDA_MODEL)


    names, name2vec, indexing = construct_mapping_from_overlap()

    # print compare_two_subreddit_similarity('technology', 'apple', name2vec)

    """
    each user(row) has fields ["name", "dom_topics", "dom_topic_str", "score", "mapped_score", "contributions", "comments", "subreddit_num"]
    """

    # Extract score out for mapping.
    scores = []

    # Add field "dom_topic_str" to the dictionary.
    topic2str = defaultdict(str)
    for i in range(100):
        topic2str[i] = ' + '.join(map(lambda x: unicode(x[0], "utf-8", errors="ignore"), ldamodel.show_topic(i, topn=4)))

    for name, obj in author_stats.iteritems():
        topic_str = [u"({0}, {1})".format(topic2str[tup[0]], tup[1]) for tup in obj['dom_topics']]
        author_stats[name]['dom_topics_str'] = topic_str
        scores.append(obj['score'])

    scale = interp1d([min(scores), max(scores)],[1,100])

    # Add mapped_score, score_by_overlap, mapped_score_by_overlap into the object.
    scores_by_overlap = []

    # Add score computed by entropy.
    scores_by_entropy = []

    # sim_names, sim_matrix = compare_subreddits_similarity_batch(name2vec)
    # print sim_names, sim_matrix

    for name, obj in author_stats.iteritems():
        author_stats[name]['mapped_score'] = scale(obj['score'])
        active_contributions = [(i, j) for i,j in obj['contributions'].iteritems() if j > 1]
        # active_contributions = filter(lambda x: x[1] > 1, obj['contributions']) # filter those minute contributions.
        # print active_contributions
        score_by_overlap = 0
        valid_scores = 0
        comb = list(itertools.combinations(active_contributions, 2)) # return topic index permutation.
        if len(comb) > 0:
            for sub1, sub2 in comb:
                # print sub1, sub2, compare_two_subreddit_similarity(sub1, sub2, name2vec)
                weight = math.sqrt(sub1[1] * sub2[1])
                sim = compare_two_subreddit_similarity(sub1[0], sub2[0], name2vec)[0][0]
                # print(sub1, sub2, sim)
                if sim > -1:
                    score_by_overlap += weight * sim # cosine similarity
                    valid_scores += weight
            if valid_scores > 0:
                score_by_overlap = score_by_overlap / valid_scores
        author_stats[name]['score_by_overlap'] = score_by_overlap
        
        entropy_score = entropy(map(lambda x: x[1], active_contributions))
        author_stats[name]['score_by_entropy'] = entropy_score
        # print(name, score_by_overlap, entropy_score)
        # print(name, score_by_overlap)
        scores_by_overlap.append(score_by_overlap)
        scores_by_entropy.append(entropy_score)

    scale_by_overlap = interp1d([min(scores_by_overlap), max(scores_by_overlap)],[1,100])
    scale_by_entropy = interp1d([min(scores_by_entropy), max(scores_by_entropy)],[1,100])

    for name, obj in author_stats.iteritems():
        author_stats[name]['mapped_score_by_overlap'] = scale_by_overlap(obj['score_by_overlap'])
        author_stats[name]['mapped_score_by_entropy'] = 101 - scale_by_entropy(obj['score_by_entropy'])
        if author_stats[name]['mapped_score_by_overlap'] == 1:
            author_stats[name]['mapped_score_by_overlap'] = -1 # meaning data too few.
        author_stats[name]['contributions'] = sorted(obj['contributions'].iteritems(), key=itemgetter(1), reverse=True)
    
    return author_stats


def write_dict_data_to_csv_file(csv_file_path, dict_data):
    csv_file = open(csv_file_path, 'wb')
    writer = csv.writer(csv_file, dialect='excel')
    
    headers = dict_data[dict_data.keys()[0]].keys()
    writer.writerow(headers)

    for key, value in dict_data.items():
        # print key, value
        if isinstance(value['subreddit_num'], int): # filter malformed field.
            line = []
            for field in headers:
                if field == 'comments':
                    res = value['comments'][:20]
                    line.append(res)
                else:
                    line.append(value[field])
            writer.writerow(line)
        
    csv_file.close()

# write_dict_data_to_csv_file(AUTHOR_CSV, author_stats)

