import sqlite3
from typing import List, Optional

QUERIES = [
    """CREATE TABLE countries (
        name    VARCHAR NOT NULL,
        capital VARCHAR NOT NULL
    )""",
    """CREATE TABLE capitals (
        name VARCHAR  NOT NULL,
        lat  REAL     NULL,
        lon  REAL     NULL
    )""",
    """CREATE TRIGGER add_capital AFTER INSERT ON countries  
    BEGIN  
        INSERT INTO capitals(name) VALUES (new.capital);  
    END;""",
    "INSERT INTO countries (name, capital) VALUES ('Peru', 'Lima'), ('UK', 'London')",
]


def init_db(conn: sqlite3.Connection, queries: List[str] = QUERIES) -> Optional[Exception]:
    cur = conn.cursor()
    try:
        for q in queries:
            cur.execute(q)
    except Exception as e:
        return e
