from contextlib import contextmanager
import sqlite3

from .interface import Rows


class SQLite:
    def __init__(self, connstr: str) -> None:
        self.connstr = connstr

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self.connstr)
        try:
            cur = conn.cursor()
            yield cur
        except Exception as e:
            print(repr(e))
        else:
            conn.commit()
        finally:
            conn.close()

    def select(self, query: str) -> Rows:
        with self._get_cursor() as cur:
            return cur.execute(query).fetchall()

    def insert(self, query: str, rows: Rows) -> int:
        with self._get_cursor() as cur:
            return cur.executemany(query, rows).rowcount

    def delete(self, query: str) -> int:
        with self._get_cursor() as cur:
            return cur.execute(query).rowcount
