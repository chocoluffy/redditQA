# Methods

In order to better evaluate the similarity and cohesiveness between different subreddit tributes and authors, we devised two embeddings based on the public reddit comments data: [1] A subreddit embeddings, produced by LSA(Latent Semantic Analysis) on authors level, and [2] a comment topic embeddings, by LDA(Latent Dirichlet Allocation).

## Subreddit embeddings by LSA

Apart from training LDA topic model, we can also construct a vector representation for each subreddit by using LSI(Latent Semantic Indexing). The basic idea is to construct a co-occurrence matrix for subreddit and reddit author, so that each entry represent the number of comments this reddit author contributes to subreddit. We then apply PCA(Primary Component Analysis) on the co-occurrence matrix to reduce the dimensions, and obtained a condense vector representation for each subreddit. In this sense, we can evaluate the similarity between different subreddits by examining its sharing contributing authors with other subreddits, based on the assumption that if two different subreddits shares a lot of unique authors in common, then these different subreddits are similar to each other at the content level. 

In our actual experiments, we uses 2133 subreddits as primary basis, which results in a vector of length 2133, with each digit the number of shared authors between two different subreddits. We obtained our raw data from Google's [BigQuery](https://github.com/lmcinnes/subreddit_mapping/blob/master/BigQuery_queries.sql). It gives the number of overlapped unique commenters between each two subreddits, and has 56187 unique top subreddits in total. After running PCA at our side, we reduce the subreddit vector dimension to 500 for the convenience of computation.

## Topic embeddings by LDA

Given reddit comments data, we are able to train a topic model on the comments text using methods such as LDA. It empowers researchers to find the underlying topics for massive subreddits given its unique conversation inside the community. 

The first step is to quantify and evaluate the similarity and clustering effect between different subreddits in the level of topics. We trained our LDA model(topic number N = 100) on the 31G pre-processed reddit comment data at June, 2015. Before training the actual model, we first pre-processing the raw comment data. We aggregate the comment data in the level of subreddits and select the top 2500 voted comments for each different subreddits and concatenated them together as the raw text documents. We then apply common text cleaning methods in sequences, such as special characters, stop words and punctuations removal, word stemming. Additionally, we also skim through the document and extract the most frequent bi-grams(appears in document more than 20 times) and append them back to the documents.

## Three evaluation methods

Given the progress we have made so far, we are able to further infer reddit authors's generalist and specialist level based on their contributions to different subreddits. We device a score to quantify such evalution, named GS score, that ranges from 0 to 100, and the higher the score is, the more special and focused interests of this reddit author. We devised such measurement from three different perspectives: [1] Weighted similarity of dominant topics from each author's contributions, [2] weighted similarity of different subreddits by counting overlapping authors, and [3] entropy value from their contribution distribution.

![combined-gs-score](https://github.com/chocoluffy/redditQA/blob/master/9-Summary/images/combined-gs-score.jpg)