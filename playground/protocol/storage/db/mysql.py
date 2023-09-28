from contextlib import contextmanager

from mysql.connector import connect, Error as ErrorMySQL

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
        except ErrorMySQL as e:
            print("MySQL ERROR: %s" % e)
        except Exception as e:
            # FIXME
            print(repr(e))
            exit(1)
        else:
            conn.commit()
        finally:
            conn.close()

    def select(self, query: str) -> Rows:
        with self._get_cursor() as cur:
            cur.execute(query)
            return list(cur.fetchall())

    def insert(self, query: str, rows: Rows) -> int:
        with self._get_cursor() as cur:
            cur.executemany(query, rows)
            return cur.rowcount

    def delete(self, query: str) -> int:
        with self._get_cursor() as cur:
            cur.execute(query)
            return cur.rowcount
