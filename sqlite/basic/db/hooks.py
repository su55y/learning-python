import sqlite3
import logging
import os.path
from typing import List

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
