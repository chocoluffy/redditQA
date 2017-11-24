```python
"""
Global stats:
    - Data:
        - 31GB, 1-month subreddit data
    
    - LDA trained on subreddit comments:
        - Pick top 1/3 subreddit with largest comments. Concatenated top 2500 upvoted comments as document.
        - Train on 100 topics.
        - Each subreddit(document) has a distribution of topics, topics have similarity.
    
    - LSA trained on author co-occurrence matrix:
        - Similarity between subreddit equals cosine similarity of their author overlap vector.

    - Entropy:
        - Produce score based on their contribution distribution.
        - Expected to err in balanced distribution cases. 

    - Current situation:
        - 28080 subreddits in total, reversed by the top 1/3 active users.
        - Pick 2%(569) most involve subreddits from the total.
    
    - Improvement:
        - Calculate scores for all users, based on their contributions.
            - LDA infer all subreddits.
        - Aggregate on subreddit, then obtain score from its involved authors.

"""


"""
Each subreddit's information lookup, contains fields:
    - scores_by_lda: list of int.
    - scores_by_overlap
    - scores_by_entropy
    - elite_scores_lda: int.
    - elite_scores_overlap
    - elite_scores_entropy
"""
reddit = pickle.load(open(REDDIT_ALL, 'rb'))
print("reddit stats loaded...")

"""
Each author's information lookup, contains fields:
    - contributions_by_count
    - contributions (by total votes)
"""
author_stats = pickle.load(open(AUTHOR_STATS, 'rb'))
print("author stats loaded...")

"""
Construct analysis dictionary
    - reddit name (pick the top 2% most involved reddit)
    - relative value: elite score - common score
    - percentage of the elite's most active subreddit equals the same one.
    - involvement (most active author involves 100~500 comments in total, least elite involves 20~100)
"""
```