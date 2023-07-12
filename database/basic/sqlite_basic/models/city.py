from dataclasses import dataclass

from math import asin, cos, radians, sin, sqrt
from typing import Self

EARTH_RADIUS = 6371


@dataclass
class City:
    name: str
    lat: float
    lon: float

    # source https://realpython.com/python-data-classes/#adding-methods
    def distance_to(self, other: Self) -> int:
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (
            sin((phi_2 - phi_1) / 2) ** 2
            + cos(phi_1)
            * cos(phi_2)
            * sin((radians(other.lon) - radians(self.lon)) / 2) ** 2
        )
        return round(2 * EARTH_RADIUS * asin(sqrt(h)))
