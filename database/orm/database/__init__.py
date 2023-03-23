from os import getenv

from sqlalchemy import DDL, text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.mapper import event

from .models import Base, Country

engine = create_engine(getenv("DB_CONN_STR", "sqlite:///test.db"), echo=True)
after_insert_country = text(
    """
CREATE TRIGGER IF NOT EXISTS after_insert_country
AFTER INSERT ON tb_countries FOR EACH ROW
BEGIN
    INSERT INTO tb_capitals (name, country_id) VALUES (NEW.capital, NEW.id);
END;
"""
)
after_update_country = text(
    """
CREATE TRIGGER IF NOT EXISTS after_update_country
AFTER UPDATE ON tb_countries FOR EACH ROW
BEGIN
    UPDATE tb_capitals SET name=NEW.capital WHERE country_id = NEW.id;
END;
"""
)

# ... it's removed like this

Base.metadata.create_all(engine)

Session = sessionmaker(engine)
with Session() as s:
    s.execute(after_insert_country)
    s.execute(after_update_country)
    s.commit()

__all__ = ["Session"]
