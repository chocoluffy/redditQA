# Abstract

# Introduction


# Related Work


# Method

In order to better evaluate the relationships between different subreddits and reddit authors for later work on author specialty inference, we experimented different methods and their combinations in text mining and topic model such as LDA(Latent Dirichlet Allocation), LSI(Latent Semantic Indexing), TF-IDF(Term Frequency–Inverse Document Frequency) and so on. 

## Subreddit Topic Model

Given reddit comments data, we are able to train a topic model on the comments text using methods such as LDA. It empowers researchers to find the underlying topics for massive subreddits given its unique conversation inside the community. 

The first step is to quantify and evaluate the similarity and clustering effect between different subreddits in the level of topics. We trained our LDA model(topic number N = 100) on the 31G pre-processed reddit comment data at June, 2015. 

### Text Pre-processing

During the pre-processing step, we aggregate the comment data in the level of sureddits and select the top 5000 voted comments for each different subreddits and concatenated them together as the raw text documents. We then apply common text cleaning methods in sequences, such as special characters, stop words and punctuations removal, word stemming. Additionally, we also skim through the document and extract the most frequent bigrams(appears in document more than 20 times) and append them back to the documents.

In order to further alleviate the impact of insignificant words on the final topic model, we then apply TF-IDF to filter such words when they either appear in less than 20 subreddits, or more than 50% of all the reddit documents. These parameters are selected based on experiments performance. 

### T-SNE Visualization

After cleaning the text data, we train our LDA model and use it to infer topic distribution vector for each different subreddits. We further apply T-SNE on each subreddit's topic distribution vector to visualize their spatial distribution in two-dimensional level. Some interesting clustering results are observed.

![pretty](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full.png)

For example, we can find from the figure that several topic-dominated tributes are formed, such as "Gaming", "Anime and Science", "Daily Life Topics and Funny Jokes"

![game](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/game-cluster.png)

![anime](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/anime%26science-cluster.png)


![life](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/daily-life-jokes-cluster.png)

The interesting clustering observations indicates that topic model is a potential powerful tool to infer different relationships between different subreddits given their own intrinsic text conversation customs. We further take advantage of this idea and extends it to infer relationships between different reddit authors.

## Reddit Author Model



# Evaluation

# Conclusion