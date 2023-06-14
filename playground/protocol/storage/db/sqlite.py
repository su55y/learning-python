from .interface import Rows


class SQLite:
    def select(self, query: str) -> Rows:
        ...

    def insert(self, query: str, rows: Rows) -> int:
        ...

    def delete(self, query: str) -> int:
        ...
