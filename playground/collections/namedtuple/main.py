from collections import namedtuple
import sqlite3

User = namedtuple("User", "id, name, age")

CREATE_TABLE = """
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)"""


def test(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(CREATE_TABLE)

    name, age = "John Doe", 30
    cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, age))
    assert cur.rowcount == 1, f"{cur.rowcount=}"

    row = cur.execute("SELECT * FROM users WHERE id = 1 LIMIT 1").fetchone()

    user = User._make(row)
    print("name: %r, age: %r" % (user.name, user.age))
    assert user.name == name, f"{user.name=}"
    assert user.age == age, f"{user.age=}"


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    try:
        test(conn)
    except Exception as e:
        print("SQL Error: %s" % e)
    finally:
        conn.close()
