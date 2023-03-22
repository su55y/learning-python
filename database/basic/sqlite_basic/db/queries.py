TB_COUNTRIES_SQL = """
    CREATE TABLE countries (
        name    VARCHAR NOT NULL,
        capital VARCHAR NOT NULL
    )"""

TB_CAPITALS_SQL = """
    CREATE TABLE capitals (
        name VARCHAR  NOT NULL,
        lat  REAL     NULL,
        lon  REAL     NULL
    )"""

AFTER_COUNTRY_INSERT_TRIGGER_SQL = """
    CREATE TRIGGER add_capital
        AFTER INSERT ON countries  
    BEGIN  
        INSERT INTO capitals(name) VALUES (new.capital);  
    END;  
"""

COUNTIES_INSERT_SQL = f"""
    INSERT INTO countries VALUES
        ("Peru", "Lima"),
        ("UK",   "London")
"""
