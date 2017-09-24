import pymongo
import pandas as pd
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(style="whitegrid", color_codes=True)
client = MongoClient('mongodb://localhost:27017/')
db = client.test
collection = db.docs_l2
pipe = [
    {'$group': {
        '_id': '$subreddit',
        'authors': { '$addToSet': '$name'},
        'comments': {'$addToSet': '$body'},
        'upsAvg': { '$avg': '$ups' },
        'controversiality': { '$avg': '$controversiality'},
        'gildedAvg': { '$avg': '$gilded' }
        }
    },
    {'$addFields': { 'commentsCount': { '$size': "$comments" } } },
    {'$addFields': { 'authorsCount': { '$size': "$authors" } } },
    {'$project':{ 'authors': 0, 'comments': 0 } } ,
    {'$sort': {'commentsCounts': -1}},
    {'$limit': 200}
]
# data = pd.DataFrame(list(collection.find()))
# data = pd.DataFrame(list(collection.aggregate(pipeline = pipe, allowDiskUse = True)))

# Print pandas dataset.
# with pd.option_context('display.max_rows', 5, 'display.max_columns', None):
#     print(data)

# Draw linear regression form of commentsCount vs upsAvg.
# sns.lmplot(x='commentsCount', y='upsAvg', data=data)

# Draw scatter plot
x = []
y = []
r = []
labels = []
for document in collection.aggregate(pipeline = pipe, allowDiskUse = True):
    x.append(document["commentsCount"])
    y.append(document["authorsCount"])
    r.append(document["upsAvg"])
    labels.append(document["_id"])

fig = plt.figure(figsize=(16, 16)) 
ax = fig.add_subplot(111)
ax.set_xlabel('# comments')
ax.set_ylabel('# authors')

import matplotlib.cm as cm
colors = cm.rainbow(np.linspace(0, 1, len(labels)))

print x, y, labels
r_avg = reduce(lambda x, y: x + y, r) / len(r)
for i in range(len(x)):
    sct = plt.scatter(x[i],y[i], color=colors[i], s=float(r[i])*20, linewidths=2, edgecolor='w')
    sct.set_alpha(0.75)
    if float(r[i]) > r_avg: # [OPTION] decide whether to show high-frequent words annotation or low-frequent ones.
        plt.annotate(labels[i],
                    xy=(x[i], y[i]),
                    xytext=(5, 2),
                    textcoords='offset points',
                    ha='right',
                    va='bottom')

plt.show()
# result = data.pivot(index='_id', columns='upsAvg', values='commentsCount')
# sns.heatmap(result, annot=True, fmt="g", cmap='viridis')
# plt.show()


