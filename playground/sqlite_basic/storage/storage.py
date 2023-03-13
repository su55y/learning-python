from contextlib import contextmanager
import logging
import sqlite3


class Storage:
    def __init__(self, file: str) -> None:
        self._file = file

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self._file)
        try:
            yield conn.cursor()
        except Exception as e:
            logging.error(e)
        finally:
            conn.commit()
            conn.close()

    def select(self):
        with self._get_cursor() as cur:
            cur.execute("SELECT * FROM tb_persons")
            return cur.fetchall()

    def insert(self, rows):
        try:
            with self._get_cursor() as cur:
                cur.executemany("INSERT INTO tb_persons VALUES(:name, :age)", rows)
                return cur.rowcount
        except Exception as e:
            logging.error(e)
            return -1
