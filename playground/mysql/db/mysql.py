from mysql.connector import connect, Error
from typing import Any, List, Tuple
from logging import info


def init_db(
    host: str, port: str, user: str, password: str, database: str, force=False
) -> Error | None:
    try:
        with connect(host=host, port=port, user=user, password=password) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE {'IF NOT EXISTS' if not force else ''} {database}"
                )
    except Error as e:
        return e


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

    def create_table(
        self, tb_name: str, fields: List[str], force=False
    ) -> Error | None:
        query = f"CREATE TABLE {'IF NOT EXISTS' if not force else ''} {tb_name} ({', '.join(fields)})"
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
        except Error as e:
            return e

    def select(
        self, tb_name: str, cols=None, where=None, limit=None
    ) -> Tuple[Any, Error | None]:
        cols_str = "*" if not cols else ", ".join(cols)
        query = f"SELECT {cols_str} FROM {tb_name}{'' if not where else ' WHERE '+where}{'' if not limit else ' LIMIT '+limit}"
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall(), None
        except Error as e:
            return None, e

    def insert_row(
        self, tb_name: str, cols: List[str], vals: Tuple[str, str]
    ) -> Error | None:
        cols_str = ", ".join(cols)
        vals_str = ", ".join(list(["%s" for _ in range(len(cols))]))
        query = f"INSERT INTO {tb_name} ({cols_str}) VALUES({vals_str})"
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, vals)
                    conn.commit()
        except Error as e:
            return e

    def insert(
        self,
        tb_name: str,
        cols: List[str],
        vals: List[Tuple[str, str] | Tuple[str, str]],
    ) -> Tuple[int, Error | None]:
        cols_str = ", ".join(cols)
        vals_str = ", ".join(list(["%s" for _ in range(len(cols))]))
        query = f"INSERT INTO {tb_name} ({cols_str}) VALUES({vals_str})"
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.executemany(query, vals)
                    conn.commit()
                    return cursor.rowcount, None
        except Error as e:
            return 0, e

    def update(
        self, tb_name: str, cols: List[str], where: List[str], vals: List[str]
    ) -> Tuple[int, Error | None]:
        cols_str = ", ".join(list(map(lambda r: f"{r}=%s", cols)))
        where_str = " and ".join(list(map(lambda w: f"{w}=%s", where)))
        query = f"UPDATE {tb_name} SET {cols_str} WHERE {where_str}".strip()
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, vals)
                    conn.commit()
                    return cursor.rowcount, None
        except Error as e:
            return 0, e

    def delete(
        self, tb_name: str, where: List[str], vals: List[str]
    ) -> Tuple[int, Error | None]:
        where_str = " and ".join(list(map(lambda w: f"{w}=%s", where)))
        query = f"DELETE FROM {tb_name} WHERE {where_str}".strip()
        info(f"try query: '{query}'")
        try:
            with self._open_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, vals)
                    conn.commit()
                    return cursor.rowcount, None
        except Error as e:
            return 0, e
