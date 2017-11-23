## Summary

A series of incremental experiments conducted on reddit comments, from 4G, 8G to 31G(one month data).

### Author

We can infer reddit authors's generalist/specialist score from three dimensions:
- weighted similarity of dominant topics from each author's contributions.
- weighted similarity of different subreddits by counting overlapping authors.
- entropy value from their contribution distribution.

And in the process, we implement two embeddings on the data:
- subreddit vector, by LSA on authors level.
- topic vector, by LDA.

### Subreddits

Given involved authors' scores, we can calculate average generalist/specialist score for each subreddit, and furthermore, find out the elite group(with the most upvoted contributions), and calculate score to examine if a pre-known generalist/specialist can be successful in such env.

### Distribution

![elite and all average](https://github.com/chocoluffy/redditQA/blob/master/6-Word2Vec/results/common-elites-score.png)

- The distribution indicates, in some subreddits, the elites exhibit different loyalty traits than common people. One interesting finding is the elite line has a slope saliently higher than 1, meaning the elite easily goes to extreme compared with the common. If the subreddit is generally dominated by specialist, then sorry the elite of this subreddit is more specialist! The converse statement also holds true. The elite tends to be an extreme form of such subreddit. 

- As expected, methods by LDA and LSA are able to correct some low score calculated by entropy. As people with equally approximate contribution may be a potential specialist if his subreddits are similar to each other.

- Three plots focus on the same elite groups, as we define elites by the most active contributions. The difference is that each person will has different score under these three standards. 

(above is the general summary of achievements so far.)
---

## Progress

- Correct the csv data from last week, including analysis for each author and each subreddit in `./results`.

- Reproduce the experiment documented from [dissecting-trumps-most-rabid-online-following/](https://fivethirtyeight.com/features/dissecting-trumps-most-rabid-online-following/).

> Upon this point, we have methods to obtain subreddit vector(by LSA), topic vector(by LDA) and word vector(by word2vec).

## Task1: Generalist/Specialist Score 

### Author perspective

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



### Subreddit perspective

[csv file](https://github.com/chocoluffy/redditQA/blob/master/6-Word2Vec/results/each_subreddit_author_distribution.csv)

- name 
- involvements: the most active author and their contribution count under this subreddit.
- total_author_count: the total number of unique authors.
- scores: average score of each author.
- dom_topic
- dom_topic_str

![subreddit](https://ww3.sinaimg.cn/large/006tKfTcgy1fl4naonfrrj31kw0hu4pj.jpg)


## Task2: Subreddit Similarity

### Subreddit Arithmetic with Gensim's LSA

Data preprocessing, TF-IDF transformation(better than not), LSI training(with topics = 200).

- r/worldnews - r/news

[(u'worldnews', 0.68611687), (u'arabs', 0.67156976), (u'Israel', 0.62338132), (u'worldpolitics', 0.59384269), (u'syriancivilwar', 0.48967499), (u'european', 0.48101518), (u'kurdistan', 0.47840986), (u'indianews', 0.4467034), (u'india', 0.44170839), (u'pakistan', 0.42912072)]

- r/weightlifting + r/running

[(u'crossfit', 0.88934195), (u'bodyweightfitness', 0.85599089), (u'weightroom', 0.83863521), (u'Weakpots', 0.81403542), (u'bodybuilding', 0.80674154), (u'weightlifting', 0.8024466), (u'powerlifting', 0.79955077), (u'xxfitness', 0.79556072), (u'Rowing', 0.75653619), (u'Fitness', 0.7504124)]

![example](https://ww1.sinaimg.cn/large/006tKfTcgy1fl44ta4fjpj311w0smjv5.jpg)

### with Article suggestions

![explanation](https://ww1.sinaimg.cn/large/006tKfTcgy1fl45czem1vj313y0h244h.jpg)

Basically, it uses 2133 subreddits as primary basis, which results in a vector of length 2133, with each digit the number of shared commenters between these two subreddits. 

The raw data, as suggested from Google [BigQuery](https://github.com/lmcinnes/subreddit_mapping/blob/master/BigQuery_queries.sql)

It gives the number of overlapped unique commenters between each two subreddits, finally 56187 subreddits in total.

-> By grouping, pivoting data into matrix, normalization, and dimension reduction to 500. 

### Result Compare

- r/politics - r/Feminism

(**'result by LSI: '**, [(u'politics', 0.6429922), (u'progressive', 0.59399098), (u'askaconservative', 0.48073345), (u'ShitPoliticsSays', 0.47253069), (u'PoliticalDiscussion', 0.45274672), (u'forwardsfromgrandma', 0.41883612), (u'Conservative', 0.41036281), (u'Libertarian', 0.38884613), (u'nyc', 0.38836086), (u'ShitRConservativeSays', 0.36959952)])

(**'result by finding overlap commenters: '**, [('Republican', 0.37096062), ('Conservative', 0.3645336), ('The_Donald', 0.36203671), ('predictit', 0.36044911), ('republicans', 0.35726255), ('BernieSandersSucks', 0.35204911), ('BrookeMarks', 0.3510778), ('IDontLikeRPolitics', 0.34955251), ('nfl', 0.34289247), ('QuarkCoin', 0.3424975)])

- r/The_Donald - r/politics

(**'result by LSI: '**, None)

(**'result by finding overlap commenters: '**, [('EnoughAntifaSpam', 0.47904247), ('Donsguard', 0.47360644), ('Bigly', 0.43075886), ('gooddoggos', 0.4281798), ('TheRightBoycott', 0.40935427), ('Gamemetahaus', 0.40908358), ('RedPillReality', 0.40160739), ('IranianAtheists', 0.39918998), ('ranked312', 0.39918998), ('TrumpLivesMatter', 0.39918998)])

- r/AskThe_Donald - r/politics

(**'result by LSI: '**, None)

(**'result by finding overlap commenters: '**, [('IranianAtheists', 0.78310621), ('ranked312', 0.78310621), ('TrumpLivesMatter', 0.78310621), ('AskAsians', 0.78131819), ('gooddoggos', 0.77355605), ('GlossyPodcast', 0.73881674), ('EnoughAntifaSpam', 0.68032324), ('hotsreplaydata', 0.66686326), ('highjump', 0.6042937), ('MyPr0n', 0.58099365)])

- r/anime + r/science 【Cool~】

(**'result by LSI: '**, [(u'anime', 0.83610475), (u'TrueAnime', 0.80928802), (u'Animesuggest', 0.80773562), (u'hentai', 0.67106557), (u'sailormoon', 0.64929271), (u'fatestaynight', 0.63300067), (u'science', 0.62421095), (u'visualnovels', 0.5954234), (u'Toonami', 0.57869101), (u'TokyoGhoul', 0.56923985)])

(**'result by finding overlap commenters: '**, [('TrueAnime', 0.87909448), ('Animesuggest', 0.87391996), ('todayilearned', 0.87237281), ('Showerthoughts', 0.86084092), ('explainlikeimfive', 0.86064804), ('funny', 0.85838616), ('IAmA', 0.85830939), ('worldnews', 0.85763919), ('thebutton', 0.85618025), ('bestof', 0.85596949)])

Try more on ipython, run `%load lsi.py`, then `test(subreddit1, subreddit2, if_add_ops)`.