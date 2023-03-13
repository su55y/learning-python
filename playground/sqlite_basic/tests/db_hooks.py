import sqlite3
import logging
import os

DB_FILE = "test.db"
CREATE_TABLE = "CREATE TABLE tb_persons (name VARCHAR, age SMALLINT CHECK (age >= 0))"
DROP_TABLE = "DROP TABLE tb_persons"


def execute(query: str) -> bool:
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute(query)
    except Exception as e:
        logging.error(e)
        return False
    return True


def init_db() -> bool:
    if os.path.exists(DB_FILE) and os.path.isfile(DB_FILE):
        logging.error("db file already exists")
        return False
    return execute(CREATE_TABLE)


def drop_table() -> bool:
    return execute(DROP_TABLE)


def drop_database() -> bool:
    if not os.path.exists(DB_FILE):
        logging.warning(f"{DB_FILE} not exists")
        return False

    if not os.path.isfile(DB_FILE):
        logging.warning(f"{DB_FILE} not file")
        return False

    try:
        os.remove(DB_FILE)
    except Exception as e:
        logging.error(e)
    else:
        return True
    return False
