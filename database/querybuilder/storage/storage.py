from contextlib import contextmanager
import logging
import sqlite3
from typing import List, Tuple

from pypika import SQLLiteQuery as Query, Table
from pypika.dialects import Term

LOG_FMT = "[%(asctime)-.19s %(levelname)-.4s] %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"


def default_logger():
    log = logging.Logger(__name__)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler("storage.log")
    fh.setFormatter(logging.Formatter(LOG_FMT))
    log.addHandler(fh)
    return log


class Storage:
    def __init__(self, file: str, logger=default_logger()) -> None:
        self._file = file
        self._log = logger

    @contextmanager
    def _get_cursor(self):
        conn = sqlite3.connect(self._file)
        try:
            yield conn.cursor()
        except Exception as e:
            self._log.error(e)
            raise e
        finally:
            conn.commit()
            conn.close()

    def select(
        self,
        tb_name: Table,
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
                self._log.debug(query.get_sql())
                cur.execute(query.get_sql())
                return cur.fetchall(), None
        except Exception as e:
            self._log.error(e)
            return [], e

    def insert(
        self, tb_name: Table, vals: List, cols: List[str] | None = None
    ) -> Tuple[int, Exception | None]:
        query = Query.into(tb_name)
        if cols:
            query = query.columns(*cols)

        query = query.insert(*vals)

        try:
            with self._get_cursor() as cur:
                self._log.debug(query.get_sql())
                cur.execute(query.get_sql())
                return cur.rowcount, None
        except Exception as e:
            self._log.error(e)
            return 0, e

    def update(
        self,
        tb_name: Table,
        vals: List,
        where: Term | List[Term],
    ) -> Tuple[int, Exception | None]:
        query = Query.update(tb_name)
        if isinstance(where, List):
            for w in where:
                query = query.where(w)
        else:
            query = query.where(where)

        for k, v in vals:
            query = query.set(k, v)

        try:
            with self._get_cursor() as cur:
                self._log.debug(query.get_sql())
                cur.execute(query.get_sql())
                return cur.rowcount, None
        except Exception as e:
            self._log.error(e)
            return 0, e

    def delete(
        self, tb_name: Table, where: Term | List[Term]
    ) -> Tuple[int, Exception | None]:
        query = Query.from_(tb_name)
        if isinstance(where, List):
            for w in where:
                query = query.where(w)
        else:
            query = query.where(where)

        query = query.delete()
        try:
            with self._get_cursor() as cur:
                self._log.debug(query.get_sql())
                cur.execute(query.get_sql())
                return cur.rowcount, None
        except Exception as e:
            self._log.error(query.get_sql())
            return 0, e
