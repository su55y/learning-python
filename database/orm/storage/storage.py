from database import Session
from contextlib import contextmanager
from typing import Type, TypeVar, Tuple, List

from sqlalchemy import update

from database.models import Country, Capital

GeoEntity = TypeVar("GeoEntity", Country, Capital)


@contextmanager
def get_session(commit=True):
    s = Session()
    try:
        yield s
        if commit:
            s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()


class Storage:
    @staticmethod
    def select_one(
        entity_type: Type[GeoEntity], *args
    ) -> Tuple[GeoEntity, Exception | None]:
        with get_session(commit=False) as s:
            try:
                if not args:
                    return s.query(entity_type).one(), None
                else:
                    return s.query(entity_type).filter(*args).one(), None
            except Exception as e:
                return entity_type(), e

    @staticmethod
    def select(
        entity_type: Type[GeoEntity], *args
    ) -> Tuple[List[GeoEntity], Exception | None]:
        with get_session(commit=False) as s:
            try:
                if not args:
                    countries = s.query(entity_type).all()
                else:
                    countries = s.query(entity_type).filter(*args).all()
            except Exception as e:
                return [], e
            return countries, None

    @staticmethod
    def insert_many(entities: List[GeoEntity]) -> Exception | None:
        with get_session() as s:
            try:
                s.add_all(entities)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def insert_one(entity: GeoEntity) -> Exception | None:
        with get_session() as s:
            try:
                s.add(entity)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def update(entity_type: Type[GeoEntity], id: int, **kwargs) -> Exception | None:
        with get_session() as s:
            try:
                query = (
                    update(entity_type).filter(entity_type.id == id).values(**kwargs)
                )
                s.execute(query)
            except Exception as e:
                return e
            else:
                return None

    @staticmethod
    def delete(entity_type: Type[GeoEntity], id: int) -> Exception | None:
        with get_session() as s:
            try:
                s.query(entity_type).filter(entity_type.id == id).delete()
            except Exception as e:
                return e
            else:
                return None
