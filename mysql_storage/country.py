from dataclasses import dataclass
import logging as log

from pypika.dialects import Table, Term
from config import db_config
from storage import MyDB
from typing import List, Tuple


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
        self.tb_countries = Table("tb_countries")
        self.cols = list(["id", "country", "capital"])

    def select_one(self, where=None) -> Tuple[Country | None, Exception | None]:
        row, err = self.storage.select(
            self.tb_name,
            cols=None,
            where=where,
            limit=1,
        )
        if err:
            return None, err

        try:
            country = Country(*row.pop())
        except Exception as e:
            return None, e
        else:
            return country, None

    def select(self, where=None, limit=None) -> Tuple[List[Country], Exception | None]:
        rows, err = self.storage.select(
            self.tb_name,
            cols=None,
            where=where,
            limit=limit,
        )
        if err:
            return [], err

        try:
            if isinstance(rows, List) and len(rows) == 0:
                return [], None

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
        self,
        countries: List[Country] | Country,
        where: List[Term] | Term,
    ) -> Tuple[int, Exception | None]:
        if isinstance(countries, List):
            rowcount = 0
            err = None
            for c in countries:
                count, err = self.storage.update(
                    self.tb_name,
                    where=where,
                    vals=[
                        (self.tb_countries.country, c.country),
                        (self.tb_countries.capital, c.capital),
                    ],
                )
                match count:
                    case 0:
                        log.warning(f"row (where {where}) not found ({c})")
                    case -1:
                        log.warning(f"row (where {where}) not updated ({c})")
                    case _:
                        rowcount += count
                if err:
                    break

            return rowcount, err
        else:
            return self.storage.update(
                self.tb_name,
                where=where,
                vals=[
                    (self.tb_countries.country, countries.country),
                    (self.tb_countries.capital, countries.capital),
                ],
            )

    def delete(self, where: List[Term] | Term) -> Tuple[int, Exception | None]:
        return self.storage.delete(
            self.tb_name,
            where=where,
        )
