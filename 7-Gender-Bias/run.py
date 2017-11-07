# In two perspectives, word2vec and subreddit vector. To map target vectors on the gender difference axis.

import gensim
import numpy as np

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)

with open('gender_pairs.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

# print content

axis_vec = model['he'] - model['she']
axis_vec = np.asarray(axis_vec)

def projection(vec):
    a = np.asarray(vec)
    res = np.dot(a, axis_vec) / np.linalg.norm(axis_vec, 2) # project vec into gender axis defined above.
    return res

projected_vecs = [projection(model[v]) for v in content if v in model]



