QUERIES = [
    "PRAGMA foreign_keys = ON;",
    """
    CREATE TABLE if not exists tb_feeds(
        channel_id VARCHAR(24) NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL
    );""",
    """
    CREATE TABLE IF NOT EXISTS tb_entries(
        id VARCHAR(11) NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL,
        updated DATETIME NOT NULL,
        channel_id VARCHAR(24) NOT NULL REFERENCES tb_feeds(channel_id) ON DELETE CASCADE
    );""",
]
