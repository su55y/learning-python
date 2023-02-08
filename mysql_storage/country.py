from dataclasses import dataclass
from config import db_config
from storage import MyDB
from typing import List, Tuple


@dataclass(order=True, slots=True)
class Country:
    id: int
    country: str
    capital: str

    def __str__(self) -> str:
        return f"{self.country}: {self.capital}"


class CountriesStorage:
    def __init__(self):
        self.tb_name = "tb_countries"
        self.storage = MyDB(**db_config)

    def select_one(self, where=None) -> Tuple[Country | None, Exception | None]:
        row, err = self.storage.select(self.tb_name, where=where, limit=1)
        if err:
            return None, err

        try:
            country = Country(*row)
        except Exception as e:
            return None, e
        else:
            return country, None

    def select(self, where=None, limit=None) -> Tuple[List[Country], Exception | None]:
        rows, err = self.storage.select(self.tb_name, where=where, limit=limit)
        if err:
            return [], err

        try:
            # bruh
            # countries = cast(List[Country], *rows)
            countries = list([Country(*r) for r in rows])
        except Exception as e:
            return [], e
        else:
            return countries, None
