# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

# In two perspectives, word2vec and subreddit vector. To map target vectors on the gender difference axis.

import gensim
import numpy as np
import scipy

# Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./models/GoogleNews-vectors-negative300.bin', binary=True)

with open('gender_pairs.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content] 

# print content

axis_vec = model['he'] - model['she']
axis_vec = np.asarray(axis_vec).reshape(1, -1)

# def projection(vec):
#     a = np.asarray(vec)
#     res = np.dot(a, axis_vec) / np.linalg.norm(axis_vec, 2) # project vec into gender axis defined above.
#     return res.tolist()

X = [model[n] for n in content if n in model]
# Q, R = np.linalg.qr(X)
# # beta = scipy.linalg.solve_triangular(R, Q.T.dot(axis_vec))

# X_proj = Q.T.dot(X)

# print X_proj



# print projected_vecs


# Draw t-sne plot on the projected vectors.
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math

def plot(labels, vecs):

    colors = cm.rainbow(np.linspace(0, 1, len(labels)))

    tsne_results = TSNE(n_components=2, perplexity=40, verbose=2).fit_transform(vecs)

    def tsne_plot(labels, tokens):
        
        labels = labels
        tokens = tokens
        radius = []

        for name in labels:
            if name in ['men', 'women', 'boy', 'girl', 'father', 'mother']:
                radius.append(25)
            else:
                radius.append(5)
        
        tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
        new_values = tsne_model.fit_transform(tokens)

        x = []
        y = []
        for value in new_values:
            x.append(value[0])
            y.append(value[1])
            
        plt.figure(figsize=(16, 16)) 
        # fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot

        for i in range(len(x)):
            sct = plt.scatter(x[i],y[i], color=colors[i], s=radius[i], linewidths=2, edgecolor='w')
            sct.set_alpha(0.75)
            plt.annotate(labels[i].encode('utf-8'),
                        xy=(x[i], y[i]),
                        xytext=(5, 2),
                        textcoords='offset points',
                        ha='right',
                        va='bottom')
        
        plt.show()

    tsne_plot(labels, vecs)

plot(content, X)

