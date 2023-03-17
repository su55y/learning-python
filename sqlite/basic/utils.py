from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS = 6371


@dataclass
class City:
    name: str
    lat: float = 0.0
    lon: float = 0.0

    # source https://realpython.com/python-data-classes/#adding-methods
    def distance_to(self, other) -> int:
        if not isinstance(other, City):
            raise TypeError("should be type City")

        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (
            sin((phi_2 - phi_1) / 2) ** 2
            + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2) ** 2
        )
        return round(2 * EARTH_RADIUS * asin(sqrt(h)))
