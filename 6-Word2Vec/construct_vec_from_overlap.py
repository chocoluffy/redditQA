import pickle
from gensim import similarities
from collections import defaultdict

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

def find_most_similar_combined_subreddit_overlap(name1, name2, add = True, names, name2vec, indexing):
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


def test_overlap(command1, command2, if_add):
    """
    command1 = 'politics'
    command2 = 'Feminism'
    if_add = False
    """
    names, name2vec, indexing = construct_mapping_from_overlap()

    sign = " + " if if_add else " - "
    print("{0}{1}{2}:".format(command1, sign, command2))

    overlap_res = find_most_similar_combined_subreddit_overlap(command1, command2, add = if_add, names, name2vec, indexing)
    print("result by finding overlap commenters: ", overlap_res)