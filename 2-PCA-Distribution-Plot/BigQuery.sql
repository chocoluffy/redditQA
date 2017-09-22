-- Download reddit comments from https://bigquery.cloud.google.com/results/ada-translator:bquijob_f67937_15ea23069c8

SELECT RANK() OVER(ORDER BY count DESC) rank, count, comment, avg_score, count_subs, count_authors, example_id 
FROM (
  SELECT comment, COUNT(*) count, AVG(avg_score) avg_score, COUNT(UNIQUE(subs)) count_subs, COUNT(UNIQUE(author)) count_authors, FIRST(example_id) example_id
  FROM (
    SELECT body comment, author, AVG(score) avg_score, UNIQUE(subreddit) subs, FIRST('http://reddit.com/r/'+subreddit+'/comments/'+REGEXP_REPLACE(link_id, 't[0-9]_','')+'/c/'+id) example_id
    FROM [fh-bigquery:reddit_comments.2015_05]
    WHERE author NOT IN (SELECT author FROM [fh-bigquery:reddit_comments.bots_201505])
    AND subreddit IN (SELECT subreddit FROM [fh-bigquery:reddit_comments.subr_rank_201505] WHERE authors>10000)
    GROUP EACH BY 1, 2
  )
  GROUP EACH BY 1
  ORDER BY 2 DESC
  LIMIT 300
)

SELECT body comment, author, AVG(score) avg_score, UNIQUE(subreddit) subs, FIRST('http://reddit.com/r/'+subreddit+'/comments/'+REGEXP_REPLACE(link_id, 't[0-9]_','')+'/c/'+id) example_id
    FROM [fh-bigquery:reddit_comments.2015_05]
    WHERE author NOT IN (SELECT author FROM [fh-bigquery:reddit_comments.bots_201505])
    AND subreddit IN (SELECT subreddit FROM [fh-bigquery:reddit_comments.subr_rank_201505] WHERE authors>10000)
    GROUP EACH BY 1, 2

SELECT
    subreddit, GROUP_CONCAT(body) AS comments     
FROM (
    SELECT subreddit, body
    FROM [fh-bigquery:reddit_comments.2015_05]
    ORDER BY ups DESC
    LIMIT 200
)           
GROUP BY subreddit

-- working version.
SELECT
    subreddit, GROUP_CONCAT(body) AS comments, AVG(ups) AS avgups
FROM (
    SELECT subreddit, body, ups
    FROM [fh-bigquery:reddit_comments.2015_06]
    WHERE ups > 100
    LIMIT 50000
)           
GROUP BY subreddit
ORDER BY avgups DESC