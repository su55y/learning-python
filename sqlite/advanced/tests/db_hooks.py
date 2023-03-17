import sqlite3
import logging
import os

DB_FILE = "test.db"
CREATE_TABLE = "CREATE TABLE tb_persons (name VARCHAR, age SMALLINT CHECK (age > 0))"
DROP_TABLE = "DROP TABLE tb_persons"


def execute(query: str, db_file: str) -> bool:
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query)
    except Exception as e:
        logging.error(e)
        return False
    return True


def init_db(db_file=DB_FILE) -> bool:
    if os.path.exists(db_file) and os.path.isfile(db_file):
        logging.error("db file already exists")
        return False
    return execute(CREATE_TABLE, db_file)


def drop_table(db_file=DB_FILE) -> bool:
    return execute(DROP_TABLE, db_file)


def drop_database(db_file=DB_FILE) -> bool:
    if not os.path.exists(db_file):
        logging.warning(f"{db_file} not exists")
        return False

    if not os.path.isfile(db_file):
        logging.warning(f"{db_file} not file")
        return False

    try:
        os.remove(db_file)
    except Exception as e:
        logging.error(e)
    else:
        return True
    return False
