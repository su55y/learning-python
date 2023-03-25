from typing import List

from sqlalchemy import update
from sqlalchemy.orm import Session

from database.models import Capital


class CapitalStorage:
    def __init__(self, session: Session) -> None:
        self.s = session

    def select(self, *args) -> List[Capital]:
        if not args:
            return self.s.query(Capital).all()
        return self.s.query(Capital).filter(*args).all()

    def insert_many(self, capitals: List[Capital]):
        self.s.add_all(capitals)
        self.s.commit()

    def insert_one(self, capital: Capital):
        self.s.add(capital)
        self.s.commit()

    def update(self, capital: Capital):
        self.s.merge(capital)
        self.s.commit()

    def update_by_id(self, id: int, **kwargs):
        query = update(Capital).filter(Capital.id == id).values(**kwargs)
        self.s.execute(query)
        self.s.commit()

    def delete(self, id: int):
        self.s.query(Capital).filter(Capital.id == id).delete()
