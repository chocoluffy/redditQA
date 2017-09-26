Rudimentary Visual:
![raw](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/raw.png)

Make it prettier:
![pretty](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/full.png)

Examine local tribes:

- Game
![game](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/game-cluster.png)

- Anime & Science
![anime](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/anime%26science-cluster.png)

- Daily life topics & Funny jokes
![life](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/daily-life-jokes-cluster.png)

- Other small tribes (subreddits with less comments)
![small](https://github.com/chocoluffy/redditQA/blob/master/2-PCA-Distribution-Plot/results/smaller-tribes.png)

## Further Explore

Given a random subreddit, can find its semantically relevant subreddits by searching through its closest N neighbors.

-> can clustering subreddit's topic vector, (currently topic vector in length 100, the number is set by user), and 100 topics will not necessarily generate 100 local clusters, as each topic is a distribution of words, and words can repeat under different topics, thus final number of clusters N will be << 100, and can be treated as labels.

-> given cluster and labels, we can observe from the perspective of reddit users by looking at which clusters of topics they have contributed to, and form a distribution of clusters for each user.

-> and thus given each user will have a cluster vector, of length the number of clusters generated, we can form a matrix of user to cluster vector, and visualize that into 2-dimensinal bubble plots and examine how closely each user are to each other from the perspective of their contribution towards reddit community. If two users are mostly contribute to the same clusters, their cluster vector will be close and so does the points on plots.

-> 【business value】: recommend talkative friends to users! (by pairing users with utmost coverage with similar clusters) so that they can subscribe to each other's timeline or simply just spark more talks. 