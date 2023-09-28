from .db.interface import IDataBase, Rows


class Storage:
    def __init__(self, db: IDataBase) -> None:
        self.db = db

    def select(self, query: str) -> Rows:
        return self.db.select(query)

    def insert(self, query: str, rows: Rows) -> int:
        return self.db.insert(query, rows)

    def delete(self, query: str) -> int:
        return self.db.delete(query)
