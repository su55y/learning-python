from typing import List, Tuple

from sqlalchemy import update

from database.models import Country
from .storage import get_session


class CountryStorage:
    @staticmethod
    def select_one(*args) -> Tuple[Country, Exception | None]:
        with get_session(commit=False) as s:
            try:
                if not args:
                    return s.query(Country).one(), None
                else:
                    return s.query(Country).filter(*args).one(), None
            except Exception as e:
                return Country(), e

    @staticmethod
    def select(*args) -> Tuple[List[Country], Exception | None]:
        with get_session(commit=False) as s:
            try:
                if not args:
                    countries = s.query(Country).all()
                else:
                    countries = s.query(Country).filter(*args).all()
            except Exception as e:
                return [], e
            return countries, None

    @staticmethod
    def insert_many(countries: List[Country]) -> Exception | None:
        with get_session() as s:
            try:
                s.add_all(countries)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def insert_one(country: Country) -> Exception | None:
        with get_session() as s:
            try:
                s.add(country)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def update(id: int, **kwargs) -> Exception | None:
        with get_session() as s:
            try:
                query = update(Country).filter(Country.id == id).values(**kwargs)
                s.execute(query)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def delete(id: int) -> Exception | None:
        with get_session() as s:
            try:
                s.query(Country).filter(Country.id == id).delete()
            except Exception as e:
                return e
            else:
                return None
