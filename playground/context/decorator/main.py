import logging as log
from contextlib import contextmanager
from mysql.connector import connect, Error as DBException

from config import db_config


def ping_db() -> bool:
    try:
        with connect(**db_config):
            return True
    except DBException as e:
        log.error(repr(e))
    except Exception as e:
        log.error(repr(e))

    return False


@contextmanager
def open_db():
    conn = connect(**db_config)
    try:
        cursor = conn.cursor()
        yield cursor
    except DBException as e:
        log.error(f"db error: {repr(e)}")
    except Exception as e:
        log.error(f"error: {repr(e)}")
    finally:
        conn.commit()
        conn.close()


def main():
    log.basicConfig(
        level=log.INFO,
        format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
        datefmt="%H:%M:%S %d/%m/%y",
    )

    if not ping_db():
        exit(1)

    tb_name = "tb_countries"
    with open_db() as cursor:
        cursor.execute(f"select * from {tb_name};")
        log.info(cursor.fetchall())


if __name__ == "__main__":
    main()
