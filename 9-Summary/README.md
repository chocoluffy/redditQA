# Abstract

# Introduction


# Related Work


# Method

In order to better evaluate the relationships between different subreddits and reddit authors for later work on author specialty inference, we experimented different methods and their combinations in text mining and topic model such as LDA(Latent Dirichlet Allocation), LSI(Latent Semantic Indexing), TF-IDF(Term Frequency–Inverse Document Frequency) and so on. 

## Subreddit by LDA topic Model

Given reddit comments data, we are able to train a topic model on the comments text using methods such as LDA. It empowers researchers to find the underlying topics for massive subreddits given its unique conversation inside the community. 

The first step is to quantify and evaluate the similarity and clustering effect between different subreddits in the level of topics. We trained our LDA model(topic number N = 100) on the 31G pre-processed reddit comment data at June, 2015. 

### Text Pre-processing

During the pre-processing step, we aggregate the comment data in the level of sureddits and select the top 5000 voted comments for each different subreddits and concatenated them together as the raw text documents. We then apply common text cleaning methods in sequences, such as special characters, stop words and punctuations removal, word stemming. Additionally, we also skim through the document and extract the most frequent bigrams(appears in document more than 20 times) and append them back to the documents.

In order to further alleviate the impact of insignificant words on the final topic model, we then apply TF-IDF to filter such words when they either appear in less than 20 subreddits, or more than 50% of all the reddit documents. These parameters are selected based on experiments performance. 

We furthermore compare the performance of training LDA topic model with either normal BOW distribution or TF-IDF weighted distribution. Some results are shown below.

Using TF-IDF weights before feeding corpus into LDA training.
![tfidf](https://github.com/chocoluffy/redditQA/blob/master/5-Model-Inspection/results/topic_dist.png)

Normal BOW model.
![normal](https://github.com/chocoluffy/redditQA/blob/master/5-Model-Inspection/results/topic_dist_normal.png)

TF-IDF version gives more polarized results than normal BOW version, meaning its ability to classify subreddit into topics is limited, given the assumption that author's interests are balanced. Therefore, in the following experiments, we use normal BOW model to process the underlying comments corpus for LDA topic model.

### T-SNE Visualization

After cleaning the text data, we train our LDA model and use it to infer topic distribution vector for each different subreddits. We further apply T-SNE on each subreddit's topic distribution vector to visualize their spatial distribution in two-dimensional level. Some interesting clustering results are observed.

![pretty](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full.png)

For example, we can find from the figure that several topic-dominated tributes are formed, such as "Gaming", "Anime and Science", "Daily Life Topics and Funny Jokes"

![game](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/game-cluster.png)

![anime](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/anime%26science-cluster.png)


![life](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/daily-life-jokes-cluster.png)

The interesting clustering observations indicates that topic model is a potential powerful tool to infer different relationships between different subreddits given their own intrinsic text conversation customs. We further take advantage of this idea and extends it to infer relationships between different reddit authors.

## Subreddit by LSI

Apart from training LDA topic model, we can also construct a vector representation for each subreddit by using LSI(Latent Semantic Indexing). The basic idea is to construct a co-occurrence matrix for subreddit and reddit author, so that each entry represent the number of comments this reddit author contributes to subreddit. We then apply PCA(Primary Component Analysis) on the co-occurrence matrix to reduce the dimensions, and obtained a condense vector representation for each subreddit. In this sense, we can evaluate the similarity between different subreddits by examining its sharing contributing authors with other subreddits, based on the assumption that if two different subreddits shares a lot of unique authors in common, then these different subreddits are similiar to each other at the content level. 

In our actual experiments, we uses 2133 subreddits as primary basis, which results in a vector of length 2133, with each digit the number of shared authors between two different subreddits. We obtained our raw data from Google's [BigQuery](https://github.com/lmcinnes/subreddit_mapping/blob/master/BigQuery_queries.sql). It gives the number of overlapped unique commenters between each two subreddits, and has 56187 unique top subreddits in total. After running PCA at our side, we reduce the subreddit vector dimension to 500 for the convenience of computation.

## Reddit Author

Given the progress we have made so far, we implemented two embeddings on the data:
- subreddit vector, by LSA on authors level.
- topic vector, by LDA.

Therefore, it aids us to further investigate at the author side. We can infer reddit authors's generalist and specialist score from the following three dimensions:
- weighted similarity of dominant topics from each author's contributions.
- weighted similarity of different subreddits by counting overlapping authors.
- entropy value from their contribution distribution.


### Elite and Common Author Distribution

![elite and all average](https://github.com/chocoluffy/redditQA/blob/master/6-Word2Vec/results/common-elites-score.png)

The distribution indicates, in some subreddits, the elites exhibit different loyalty traits than common people. One interesting finding is the elite line has a slope saliently higher than 1, meaning the elite easily goes to extreme compared with the common. If the subreddit is generally dominated by specialist, then sorry the elite of this subreddit is more specialist! The converse statement also holds true. The elite tends to be an extreme form of such subreddit. 

As expected, methods by LDA and LSA are able to correct some low score calculated by entropy. As people with equally approximate contribution may be a potential specialist if his subreddits are similar to each other.

Three plots focus on the same elite groups, as we define elites by the most active contributions. The difference is that each person will has different score under these three standards. 

### Supporting Materials: Author

[csv file](https://github.com/chocoluffy/redditQA/blob/master/6-Word2Vec/results/updated_each_author_topic_comment.csv)

- name
- score: generalist/specialist score, higher the score, more special the author is.
- score_by_overlap: still generalist/specialist score, but using LSA on author perspective, by calculating overlapping authors.
- mapped_score: a re-scaling from the above score to 1~100, to be more intuitive.
- mapped_score_by_overlap: a re-scaling from score_by_overlap.
- dom_topics
- subreddit_num: 
- comments: top voted comments selected.
- dom_topics_str: string representation of the dominant topics.
- contributions

We infer dominant topics and score. We observe that it accords with the ground truth(the actual subreddit the author contributes to and the actual comments text).


### Supporting Materials: Subreddit

[csv file](https://github.com/chocoluffy/redditQA/blob/master/6-Word2Vec/results/each_subreddit_author_distribution.csv)

- name 
- involvements: the most active author and their contribution count under this subreddit.
- total_author_count: the total number of unique authors.
- scores: average score of each author.
- dom_topic
- dom_topic_str

![subreddit](https://ww3.sinaimg.cn/large/006tKfTcgy1fl4naonfrrj31kw0hu4pj.jpg)


## Generalist and Specialist Score





# Evaluation

# Conclusion