CREATE TABLE comments (
    id String,
    link_id String,
    parent_id String,
    author String,
    created_utc DateTime,
    body String,
    score Int64,
    controversiality Int8,
    distinguished Nullable(String),
    subreddit String
) ENGINE = MergeTree()
ORDER BY (subreddit, link_id, created_utc, id);
