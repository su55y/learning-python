from os import getenv

from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

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

after_delete_country = text(
    """
CREATE TRIGGER IF NOT EXISTS after_delete_country
AFTER DELETE ON tb_countries FOR EACH ROW
BEGIN
	DELETE FROM tb_capitals WHERE country_id = OLD.id;
END;
"""
)

_ENV_CONN_STR = "ENV_CONN_STR"
_DEFAULT_CONN_STR = "sqlite:///test.db"

engine = create_engine(getenv(_ENV_CONN_STR, _DEFAULT_CONN_STR))
Session = sessionmaker(engine)


def init_db() -> Exception | None:
    try:

        Base.metadata.create_all(engine)
        with Session() as s:
            s.execute(after_insert_country)
            s.execute(after_update_country)
            s.execute(after_delete_country)
            s.commit()
    except Exception as e:
        return e


__all__ = ["Session"]
