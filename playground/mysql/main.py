from config import db_config
from db import MyDB, init_db
from logging import INFO, basicConfig, error, info


def die(e: str):
    error(e)
    exit(1)


def main():
    basicConfig(
        level=INFO,
        format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
        datefmt="%H:%M:%S %d/%m/%y",
    )
    if err := init_db(**db_config):
        die(f"DB_CREATE_ERROR: {repr(err)}")

    my_db = MyDB(**db_config)
    tb_countries = "tb_countries"
    col_id = "id"
    col_country = "country"
    col_capital = "capital"

    if err := my_db.create_table(
        tb_name=tb_countries,
        fields=list(
            [
                f"{col_id} INT NOT NULL AUTO_INCREMENT",
                f"{col_country} VARCHAR(255) NOT NULL",
                f"{col_capital} VARCHAR(255) NOT NULL",
                f"PRIMARY KEY ({col_id})",
            ]
        ),
    ):
        die(f"CREATE TABLE ERROR: {repr(err)}")

    if err := my_db.insert_row(
        tb_name=tb_countries,
        cols=[col_country, col_capital],
        vals=("Ukraine", "Kyiv"),
    ):
        die(f"INSERT_ROW_ERROR: {repr(err)}")

    insert_count, insert_err = my_db.insert(
        tb_name=tb_countries,
        cols=[col_country, col_capital],
        vals=[("United Kingdom", "London"), ("Poland", "Warsaw"), ("India", "Delhi")],
    )
    if insert_err:
        error(f"INSERT_ERROR: {repr(insert_err)}")
    else:
        info(f"{insert_count} rows inserted")

    countries, select_err = my_db.select(tb_name=tb_countries)
    if select_err:
        error(f"SELECT_ERROR: {repr(select_err)}")
    else:
        for c in countries:
            print(c)

    update_count, update_error = my_db.update(
        tb_name=tb_countries,
        cols=[col_capital],
        vals=["New-Delhi", "India"],
        where=[col_country],
    )
    if update_error:
        error(f"UPDATE_ERROR: {repr(update_error)}")
    else:
        info(f"{update_count} rows updated")

    country, select_row_err = my_db.select(
        tb_name=tb_countries,
        cols=[col_country, col_capital],
        where=f"{col_country} = 'India'",
    )
    if select_row_err:
        error(f"SELECT_ROW_ERROR: {repr(select_row_err)}")
    else:
        for c in country:
            print(c)

    delete_count, delete_error = my_db.delete(
        tb_name=tb_countries, where=[col_country], vals=["India"]
    )
    if delete_error:
        error(f"DELETE_ERROR {repr(delete_error)}")
    else:
        info(f"{delete_count} rows deleted")

    countries2, select_err2 = my_db.select(tb_name=tb_countries)
    if select_err2:
        error(f"SELECT_ERROR: {repr(select_err)}")
    else:
        for c in countries2:
            print(c)


if __name__ == "__main__":
    main()
