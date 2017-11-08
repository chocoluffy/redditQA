import pickle
from gensim import similarities
from collections import defaultdict
import os.path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Model path.
# VERSION_PATH = './models/lsi_tfidf_topic_100'
VERSION_PATH = './models/share'

MAP_VECTORS_FROM_OVERLAP = os.path.join(VERSION_PATH, 'subreddit_vector.pkl')
OVERLAP_INDEX = os.path.join(VERSION_PATH, 'overlap.index')

def construct_mapping_from_overlap():    
    map_vectors = pickle.load(open(MAP_VECTORS_FROM_OVERLAP, 'rb'))
    names_lst, vectors_lst = [list(t) for t in zip(*map_vectors)]

    if not os.path.exists(OVERLAP_INDEX):
        index_overlap = similarities.MatrixSimilarity(vectors_lst, num_features=NUM_FEATURES_OVERLAP)
        index_overlap.save(OVERLAP_INDEX)
        print("save similarity index of vectors from shared commenters...")
    else:
        index_overlap = similarities.MatrixSimilarity.load(OVERLAP_INDEX)
        print("load similarity index of vectors from shared commenters...")


    vectors_dict = defaultdict()
    for name, vec in map_vectors:
        vectors_dict[name] = vec
    
    return names_lst, vectors_dict, index_overlap

def find_most_similar_combined_subreddit_overlap(names, name2vec, indexing, name1, name2, add = True):
    if  name1 in name2vec and name2 in name2vec:
        sub_vec1 = name2vec[name1]
        sub_vec2 = name2vec[name2]
        if add:
            comb_vec = [i+j for i, j in zip(sub_vec1, sub_vec2)]
        else:
            comb_vec = [i-j for i, j in zip(sub_vec1, sub_vec2)]
        comb_vec = [(i, vec) for i, vec in enumerate(comb_vec)]
        sims = indexing[comb_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])   
        res = map(lambda x: (names[x[0]], x[1]), sims[:10])
        return res
    else:
        print("at least one of the subreddit not found...")

def find_most_similar_algebra_subreddit_overlap(names, name2vec, indexing, name1, name2, name3):
    if  name1 in name2vec and name2 in name2vec and name3 in name2vec:
        sub_vec1 = name2vec[name1]
        sub_vec2 = name2vec[name2]
        sub_vec3 = name2vec[name3]
        comb_vec = [k-i+j for i, j, k in zip(sub_vec1, sub_vec2, sub_vec3)]
        comb_vec = [(i, vec) for i, vec in enumerate(comb_vec)]
        sims = indexing[comb_vec]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])   
        res = map(lambda x: (names[x[0]], x[1]), sims[:10])
        return res
    else:
        print("at least one of the subreddit not found...")


pair2sim = defaultdict()
def compare_two_subreddit_similarity(name1, name2, name2vec):
    """
    Construct a dictionary to cache the final similarity results. Sort two names and concat as the key.
    """
    if name1 in name2vec and name2 in name2vec:
        pair_key = ','.join(sorted([name1, name2]))
        sub_vec1 = name2vec[name1]
        sub_vec2 = name2vec[name2]
        sub_vec1 = np.array(sub_vec1).reshape((1, len(sub_vec1)))
        sub_vec2 = np.array(sub_vec2).reshape((1, len(sub_vec2)))
        if pair_key in pair2sim:
            res = pair2sim[pair_key]
        else:
            res = cosine_similarity(sub_vec1, sub_vec2)
            # print("add key", pair_key)
            pair2sim[pair_key] = res
        return res
    else:
        # print("at least one of the subreddit not found...")
        return [[-1]]


def compare_subreddits_similarity_batch(name2vec):
    names_lst = []
    vecs_lst = []
    for n, v in name2vec.iteritems():
        names_lst.append(n)
        vecs_lst.append(v)
    return names_lst, cosine_similarity(vecs_lst)


def test_overlap(command1, command2, if_add):
    """
    command1 = 'politics'
    command2 = 'Feminism'
    if_add = False
    """
    names, name2vec, indexing = construct_mapping_from_overlap()

    sign = " + " if if_add else " - "
    print("{0}{1}{2}:".format(command1, sign, command2))

    overlap_res = find_most_similar_combined_subreddit_overlap(names, name2vec, indexing, command1, command2, add = if_add)
    print("result by finding overlap commenters: ", overlap_res)
