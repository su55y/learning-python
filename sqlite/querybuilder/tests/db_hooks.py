import logging
import os
import sqlite3
from typing import List

DB_FILE = "test.db"
CREATE_TABLE = "CREATE TABLE tb_persons (name VARCHAR, age SMALLINT CHECK (age > 0))"
DROP_TABLE = "DROP TABLE tb_persons"

LOG_FMT = "[%(asctime)-.19s %(levelname)-.4s] %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"


def default_logger():
    log = logging.Logger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT))
    log.addHandler(sh)
    return log


class DBHooks:
    def __init__(self, db_file: str, log: logging.Logger = default_logger()) -> None:
        self.db_file = db_file
        self.log = log

    def _execute(self, query) -> bool:
        try:
            with sqlite3.connect(self.db_file) as conn:
                conn.execute(query)
        except Exception as e:
            self.log.error(f"{e} ({query})")
            return False
        else:
            return True

    def init_db(self, queries: List[str]) -> bool:
        for tb in queries:
            if not self._execute(tb):
                return False
        return True

    def drop_db(self) -> bool:
        if not os.path.exists(self.db_file):
            self.log.warn(f"db_file {self.db_file} not exists")
            return False
        if not os.path.isfile(self.db_file):
            self.log.warn(f"{self.db_file} is not a file")
            return False
        try:
            os.remove(self.db_file)
        except Exception as e:
            self.log.error(e)
            return False
        else:
            return True


# ------------------------------------------------------------
def execute(query: str, db_file: str) -> bool:
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query)
    except Exception as e:
        logging.error(e)
        return False
    return True


def init_db(db_file=DB_FILE, force=False) -> bool:
    if os.path.exists(db_file) and os.path.isfile(db_file):
        if not force:
            logging.error("db file already exists")
            return False
        os.remove(db_file)
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
