from contextlib import contextmanager
import logging
import sqlite3
from typing import List, Tuple


from pypika import SQLLiteQuery as Query
from pypika.dialects import Term


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

    def select(
        self,
        tb_name: str,
        cols: List[str] | None = None,
        where: List[Term] | Term | None = None,
        limit: int | None = None,
    ) -> Tuple[List, Exception | None]:
        query = Query.from_(tb_name)
        if cols and len(cols) > 0:
            query = query.select(*cols)
        else:
            query = query.select("*")

        if where:
            if isinstance(where, List):
                for w in where:
                    query = query.where(w)
            else:
                query = query.where(where)

        if limit:
            query = query.limit(limit)

        try:
            with self._get_cursor() as cur:
                cur.execute(query.get_sql())
                return cur.fetchall(), None
        except Exception as e:
            logging.error(e)
            return [], e

    def insert(
        self,
        tb_name: str,
        vals: List,
        cols: List[str] | None = None,
    ) -> Tuple[int, Exception | None]:
        query = Query.into(tb_name)
        if cols:
            query = query.columns(*cols)
        query = query.insert(*vals)

        try:
            with self._get_cursor() as cur:
                cur.execute(query.get_sql())
                return cur.rowcount, None
        except Exception as e:
            logging.error(e)
            return 0, e
