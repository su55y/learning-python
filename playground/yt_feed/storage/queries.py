QUERIES = [
    """
    CREATE TABLE IF NOT EXISTS tb_entries(
        id VARCHAR(11) NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL,
        updated DATETIME NOT NULL
    );""",
]
