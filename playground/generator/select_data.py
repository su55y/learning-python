from collections.abc import Callable
from typing import Any, List, Tuple
from mysql.connector import connect, Error as DatabaseError

import logging as log

log.basicConfig(
    level=log.INFO,
    format="[%(asctime)-.19s %(levelname)-.4s] %(message)s (%(filename)s:%(funcName)s:%(lineno)d)",
)
db_conf = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "py_test_db",
}

SELECT_QUERY = "SELECT country, capital FROM tb_countries"


def with_select(callback: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper():
        while True:
            data = None
            log.debug(SELECT_QUERY)
            try:
                with connect(**db_conf) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(SELECT_QUERY)
                        data = cursor.fetchall()
            except DatabaseError as e:
                log.error(f"DB ERROR: {repr(e)}")
            except Exception as e:
                log.error(repr(e))
            else:
                log.info(f"selected {len(data)} rows")
            finally:
                yield callback(data)

    return wrapper


@with_select
def generate_data(data: List[Tuple[str, str]] | None) -> str:
    if not data:
        return "no data"

    return "\n".join([f"{row[0]}: {row[1]}" for row in data if len(row) == 2])


data_generator = generate_data()
get_data = lambda: next(data_generator)

