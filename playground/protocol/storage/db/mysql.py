from contextlib import contextmanager

from mysql.connector import connect

from .interface import Rows


class MySQL:
    def __init__(self, **kwargs) -> None:
        self.__conf = kwargs

    @contextmanager
    def _get_cursor(self):
        conn = connect(**self.__conf)
        try:
            with conn.cursor() as cur:
                yield cur
        except:
            ...
        finally:
            conn.close()

    def select(self, query: str) -> Rows:
        with self._get_cursor() as cur:
            return cur.execute(query).fetchall()

    def insert(self, query: str, rows: Rows) -> int:
        with self._get_cursor() as cur:
            return cur.execute(query, rows).rowcount

    def delete(self, query: str) -> int:
        with self._get_cursor() as cur:
            return cur.execute(query).rowcount
