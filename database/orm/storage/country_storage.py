from typing import List

from sqlalchemy import update

from database.models import Country
from .storage import get_session


class CountryStorage:
    def select(self, *args) -> List[Country]:
        with get_session(commit=False) as s:
            if not args:
                return s.query(Country).all()
            return s.query(Country).filter(*args).all()

    def insert_many(self, countries: List[Country]):
        with get_session() as s:
            s.add_all(countries)

    def insert_one(self, country: Country):
        with get_session() as s:
            s.add(country)

    def update(self, country: Country):
        with get_session() as s:
            s.merge(country)

    def update_by_id(self, id: int, **kwargs):
        with get_session() as s:
            query = update(Country).filter(Country.id == id).values(**kwargs)
            s.execute(query)

    def delete(self, id: int):
        with get_session() as s:
            s.query(Country).filter(Country.id == id).delete()
