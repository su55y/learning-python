import sqlalchemy.orm as orm

from .base import Base


class Country(Base):
    __tablename__ = "tb_countries"
    name: orm.Mapped[str] = orm.mapped_column(primary_key=True)
    capital: orm.Mapped[str]

    def __repr__(self) -> str:
        return f"Country(name={self.name!r}, name={self.capital!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Country):
            return False
        return self.name == other.name and self.capital == other.capital
