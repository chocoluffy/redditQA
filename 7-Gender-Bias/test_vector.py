import os.path
import sys

lib_path = os.path.abspath(os.path.join('./../6-Word2Vec'))
sys.path.append(lib_path) # in order to import author_csv, which is at a upper folder.

# import construction from module.
from construct_vec_from_overlap import *

names, name2vec, indexing = construct_mapping_from_overlap()

def test_binary(command1, command2, if_add):
    sign = " + " if if_add else " - "
    print("{0}{1}{2}:".format(command1, sign, command2))
    overlap_res = find_most_similar_combined_subreddit_overlap(names, name2vec, indexing, command1, command2, add = if_add)
    print("result by finding overlap commenters: ", overlap_res)

def test_trinary(command1, command2, command3):
    print("{0} - {1} = {2} - ?:".format(command1,command2, command3))
    overlap_res = find_most_similar_algebra_subreddit_overlap(names, name2vec, indexing, command1, command2, command3)
    print("result by finding overlap commenters: ", overlap_res)



command1 = 'AskMen'
command2 = 'AskWomen'
command3 = 'The_Donald'
if_add = False

# test_binary(command1, command2, if_add)
test_trinary(command1, command2, command3)