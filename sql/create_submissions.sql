CREATE TABLE submissions (
    id String,
    name String,
    author String,
    created_utc DateTime,
    title String,
    selftext String,
    url String,
    domain String,
    url_overridden_by_dest String,
    score Int64,
    upvote_ratio Float32,
    num_comments Int64,
    subreddit_subscribers Int64,
    view_count Nullable(Int64),
    distinguished Nullable(String),
    subreddit String
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(created_utc)
ORDER BY (subreddit, created_utc, id);
