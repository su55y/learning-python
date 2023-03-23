from typing import Optional
from sqlalchemy import ForeignKey
import sqlalchemy.orm as orm

from .base import Base


class Capital(Base):
    __tablename__ = "tb_capitals"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    name: orm.Mapped[str] = orm.mapped_column(unique=True)
    lat: orm.Mapped[Optional[float]]
    lon: orm.Mapped[Optional[float]]
    country_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("tb_countries.id"))

    def __repr__(self) -> str:
        return f"Country(name={self.name!r}, lat={self.lat!r}, lon={self.lon!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Capital):
            return False
        return self.name == other.name
