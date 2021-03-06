# Methods



In order to better evaluate the similarity and cohesiveness between different subreddit tributes and authors, we devised two embeddings based on the public reddit comments data: [1] A subreddit embeddings, produced by LSA(Latent Semantic Analysis) on authors level, and [2] a comment topic embeddings, by LDA(Latent Dirichlet Allocation). Our final goal is to examine how community's level of specialty is related to its contributing authors' specialties, and throughout the experiments, we find an interesting phenomenon that the top successful authors inside a subreddit community are often having a more extreme level of specialty than their common peers. In another word, inside an interest-focused subreddit, the successful Reddit authors usually have more focused and special interests and contributions, and for an interests-general subreddit, its top authors have more general and egalitarian interests and contributions.



## Subreddit embeddings by LSA



Apart from training LDA topic model, we can also construct a vector representation for each subreddit by using LSI(Latent Semantic Indexing). The basic idea is to construct a co-occurrence matrix for subreddit and Reddit author so that each entry represents the number of comments this Reddit author contributes to subreddit. We then apply PCA(Primary Component Analysis) on the co-occurrence matrix to reduce the dimensions and obtained a condense vector representation for each subreddit. In this sense, we can evaluate the similarity between different subreddits by examining its sharing contributing authors with other subreddits, based on the assumption that if two different subreddits shares a lot of unique authors in common, then these different subreddits are similar to each other at the content level. 



In our actual experiments, we use 2133 subreddits as primary basis, which results in a vector of length 2133, with each digit the number of shared authors between two different subreddits. We obtained our raw data from Google's [BigQuery](https://github.com/lmcinnes/subreddit_mapping/blob/master/BigQuery_queries.sql). It gives the number of overlapped unique commenters between every two subreddits and has 56187 unique top subreddits in total. After running PCA at our side, we reduce the subreddit vector dimension to 500 for the convenience of computation.



## Topic embeddings by LDA



Given Reddit comments data, we are able to train a topic model on the comments text using methods such as LDA. It empowers researchers to find the underlying topics for massive subreddits given its unique conversation inside the community. 



The first step is to quantify and evaluate the similarity and clustering effect between different subreddits in the level of topics. We trained our LDA model(topic number N = 100) on the 31G pre-processed Reddit comment data at June 2015. Before training the actual model, we first pre-processing the raw comment data. We aggregate the comment data in the level of subreddits and select the top 2500 voted comments for each different subreddits and concatenated them together as the raw text documents. We then apply common text cleaning methods in sequences, such as special characters, stop words and punctuations removal, word stemming. Additionally, we also skim through the document and extract the most frequent bi-grams(appears in the document more than 20 times) and append them back to the documents.



## Three evaluation methods



Given the progress we have made so far, we are able to further infer Reddit authors' generalist and specialist level based on their contributions to different subreddits. We devise a score to quantify such evaluation, named GS score, that ranges from 0 to 100, and the higher the score is, the more special and focused interests of this Reddit author. We devised such measurement from three different perspectives: [1] LDA, using weighted similarity of dominant topics from each author's contributions, [2] entropy value from their contribution distribution, and [3] LSA, using weighted similarity of different subreddits by counting overlapping authors. Given the GS score, we calculate for each Reddit users, we are able to observe score distribution in a macro view, a.k.a from the perspective of a subreddit community, where we can see how each community differs with each other by owning authors of different level of interests. 



To further granularize community's internal structure, we also examine the groups of "elite" authors of each community, where their comments receive most upvotes in general and become successfully inside their contributing communities. We want to know if there are any relationships between elite group's specialty and its belonged community's specialty. And interestingly, we found that the elite group usually acts more biased than its common counterpart inside the same subreddit community. We can observe from the figure below that all methods indicate that the elite's slope(y-axis) is slightly greater than 1, which is the common authors(x-axis). It indicates that for a community of special and focused interests, the top successful authors are actually having more focused interests, and for a community of general interests, the top successful authors may also be more general than average. 



![combined-gs-score](https://github.com/chocoluffy/redditQA/blob/master/9-Summary/images/combined-gs-score-new.jpg)

from left to right, generated by LDA, entropy and LSA methods.