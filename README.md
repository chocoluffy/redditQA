## 1-Predict-Topics

Run TF-IDF and LSI on existing subreddit comments, and given user's new comment, try predicting and recommending subreddit.

[Predict Topics](https://github.com/chocoluffy/redditQA/tree/master/1-Predict-Topics)

## 2-PCA-Distribution-Plot

Build document-term matrix from BigQuery data, then run LDA to find topics distribution for each subreddit, and apply t-SNE dimension reduction with matplotlib visualization.

[LDA visualization](https://github.com/chocoluffy/redditQA/tree/master/2-PCA-Distribution-Plot)

## 3-Bipartite-Graph

Construct a bipartite graph between authors and topics, and propagate back and forth the labels to identify generalist/specialist among reddit authors for differnt community.

[Bipartite Graph](https://github.com/chocoluffy/redditQA/tree/master/3-Bipartite-Graph)

## 4-LDA-On-TFIDF

Fine tune the model from week3, with TF-IDF weights applied on BOW matrix but keep in same magnitude. 

[Improved LDA](https://github.com/chocoluffy/redditQA/tree/master/4-LDA-On-Tfidf)

## 5-Model-Inspection

Examine the validity of models obtained from week4, and refine models by tuning hyper-parameters.

[Model Inspection](https://github.com/chocoluffy/redditQA/tree/master/5-Model-Inspection)