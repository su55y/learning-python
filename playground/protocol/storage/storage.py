from .db.interface import IDataBase, Rows


class Storage:
    def __init__(self, db: IDataBase) -> None:
        self.db = db

    def select(self, id: int) -> Rows:
        query = "select * from table where id = %d" % id
        return self.db.select(query)

    def insert(self, rows: Rows) -> int:
        query = "insert into table values ?"
        return self.db.insert(query, rows)

    def delete(self, id: int) -> int:
        query = "delete from table whre id = %d" % id
        return self.db.delete(query)
