-- Full raw data download at here: http://files.pushshift.io/reddit/comments/

-- Big kudos for @lmcinnes's work here https://github.com/lmcinnes/subreddit_mapping/blob/master/BigQuery_queries.sql
-- Reddit has complete data hosted on Google's big query, including year level from 2005-2014, and month level for years from 2015-2017
-- Here, I try to create subreddit vector representation using LSI method, therefore, creating overlapping stats for year level data only.
-- First query need to be saved into an external table such as subreddit_author_2014
SELECT subreddit, authors, DENSE_RANK() OVER (ORDER BY authors DESC) AS rank_authors
FROM (SELECT subreddit, SUM(1) as authors
     FROM (SELECT subreddit, author, COUNT(1) as cnt 
         FROM [fh-bigquery:reddit_comments.2014] 
         WHERE author NOT IN (SELECT author FROM [fh-bigquery:reddit_comments.bots_201505])
         GROUP BY subreddit, author HAVING cnt > 0)
     GROUP BY subreddit) t
ORDER BY authors DESC;

-- Second query will read the data saved from the first query, and produce the overlapping stats table. Then save the result into csv and download.
SELECT t1.subreddit, t2.subreddit, SUM(1) as NumOverlaps
FROM (SELECT subreddit, author, COUNT(1) as cnt 
     FROM [fh-bigquery:reddit_comments.2014] 
     WHERE author NOT IN (SELECT author FROM [fh-bigquery:reddit_comments.bots_201505])
     AND subreddit IN (SELECT subreddit FROM [reddit_research.subreddit_author_2014] 
       WHERE rank_authors>200 AND rank_authors<2201)
     GROUP BY subreddit, author HAVING cnt > 10) t1
JOIN (SELECT subreddit, author, COUNT(1) as cnt 
     FROM [fh-bigquery:reddit_comments.2014]
     WHERE author NOT IN (SELECT author FROM [fh-bigquery:reddit_comments.bots_201505])
     GROUP BY subreddit, author HAVING cnt > 10) t2
ON t1.author=t2.author
WHERE t1.subreddit!=t2.subreddit
GROUP BY t1.subreddit, t2.subreddit