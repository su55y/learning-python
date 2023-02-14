from config.config import db_config
from mysql.connector import connect, Error

db_conf = db_config.copy()
db_name = db_conf.pop("database")


def execute(query: str) -> bool:
    try:
        with connect(**db_conf) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
    except:
        return False
    return True


def create() -> bool:
    queries = [
        f"CREATE DATABASE IF NOT EXISTS {db_name}",
        f"""CREATE TABLE IF NOT EXISTS {db_name}.tb_countries (\
            id int NOT NULL AUTO_INCREMENT,\
            country varchar(255) NOT NULL,\
            capital varchar(255) NOT NULL,\
            PRIMARY KEY (id)\
        )""",
    ]
    for q in queries:
        if not execute(q):
            return False
    return True


def drop() -> bool:
    return execute(f"DROP DATABASE IF EXISTS {db_name}")
