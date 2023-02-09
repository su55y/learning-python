from dataclasses import dataclass
from config import db_config
from storage import MyDB
from typing import List, Tuple
from enum import Enum


class Where(Enum):
    Id = "id=%s"
    Country = "country=%s"
    Capital = "capital=%s"


@dataclass(order=True, slots=True, eq=True)
class Country:
    id: int | None
    country: str
    capital: str

    def __str__(self) -> str:
        return f"{self.country}: {self.capital}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Country):
            return NotImplemented
        else:
            return self.country == other.country and self.capital == other.capital


class CountriesStorage:
    def __init__(self):
        self.tb_name = "tb_countries"
        self.storage = MyDB(**db_config)
        self.cols = list(["id", "country", "capital"])

    def select_one(self, where=None) -> Tuple[Country | None, Exception | None]:
        row, err = self.storage.select(self.tb_name, where=where, limit=1)
        if err:
            return None, err

        try:
            country = Country(*row.pop())
        except Exception as e:
            return None, e
        else:
            return country, None

    def select(self, where=None, limit=None) -> Tuple[List[Country], Exception | None]:
        rows, err = self.storage.select(self.tb_name, where=where, limit=limit)
        if err:
            return [], err

        try:
            countries = list([Country(*r) for r in rows])
        except Exception as e:
            return [], e
        else:
            return countries, None

    def insert(self, countries: List[Country]) -> Tuple[int, Exception | None]:
        return self.storage.insert(
            self.tb_name,
            cols=["country", "capital"],
            vals=[(c.country, c.capital) for c in countries],
        )

    def update(
        self, countries: List[Country], where: Where = Where.Id
    ) -> Tuple[int, Exception | None]:
        match (where):
            case Where.Country:
                vals = [(c.country, c.capital, c.country) for c in countries]
            case Where.Capital:
                vals = [(c.country, c.capital, c.capital) for c in countries]
            case _:
                where = Where.Id
                vals = [(c.country, c.capital, str(c.id)) for c in countries]

        return self.storage.update_all(
            self.tb_name,
            cols=["country", "capital"],
            where=where.value,
            vals=vals,
        )

    def delete(
        self, countries: List[Country], where: Where = Where.Id
    ) -> Tuple[int, Exception | None]:
        match (where):
            case Where.Country:
                vals = [(c.country,) for c in countries]
            case Where.Capital:
                vals = [(c.capital,) for c in countries]
            case _:
                vals = [(c.id,) for c in countries]

        return self.storage.delete(
            self.tb_name,
            where=where.value,
            vals=vals,
        )
