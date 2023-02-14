import logging as log
from typing import Any, List, Tuple

from mysql.connector import connect, Error
from pypika import MySQLQuery as Query
from pypika.dialects import Term


class MyDB:
    def __init__(self, host: str, port: str, user: str, password: str, database: str):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

    def _open_conn(self):
        return connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
        )

    def _execute(self, query: str, fetch=False) -> Tuple[Any, Error | Exception | None]:
        log.debug(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    if fetch:
                        rows = list(cur.fetchall())
                        return rows, None
                    conn.commit()
                    return cur.rowcount, None
        except (Error, Exception) as e:
            log.error(e)
            return None, e

    def ping(self) -> bool:
        try:
            with self._open_conn() as conn:
                conn.ping(reconnect=True, attempts=3, delay=200)
        except (Error, Exception) as e:
            if isinstance(e, Error):
                log.error(f"{e.errno}: {e.msg}")
            else:
                log.error(repr(e))

            return False

        return True

    def select(
        self,
        tb_name: str,
        cols: List[str] | None = None,
        where: List[Term] | Term | None = None,
        limit: int | None = None,
    ) -> Tuple[List[Any] | Any, Error | Exception | None]:
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

        return self._execute(query.get_sql(), fetch=True)

    def insert(
        self,
        tb_name: str,
        cols: List[str],
        vals: List[Tuple[str, str]],
    ) -> Tuple[int, Error | Exception | None]:
        query = Query.into(tb_name)
        if cols:
            query = query.columns(*cols)
        query = query.insert(*vals)

        return self._execute(query.get_sql())

    def update(
        self,
        tb_name: str,
        where: List[Term] | Term,
        vals: List[Tuple[Any, str]],
    ) -> Tuple[int, Error | Exception | None]:
        query = Query.update(tb_name)
        if isinstance(where, List):
            for w in where:
                query = query.where(w)
        else:
            query = query.where(where)

        for k, v in vals:
            query = query.set(k, v)

        return self._execute(query.get_sql())

    def delete(
        self, tb_name: str, where: List[Term] | Term
    ) -> Tuple[int, Error | Exception | None]:
        query = Query.from_(tb_name)
        if isinstance(where, List):
            for w in where:
                query = query.where(w)
        else:
            query = query.where(where)
        query = query.delete()
        return self._execute(query.get_sql())
