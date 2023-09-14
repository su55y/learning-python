from collections import namedtuple
import sqlite3

User = namedtuple("User", "id, name, age")


def test(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL)"
    )
    cur.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)", (name := "John Doe", age := 33)
    )
    row = cur.execute("select * from users where id = 1 LIMIT 1").fetchone()

    u1 = User._make(row)
    print("name: %r, age: %r" % (u1.name, u1.age))
    assert u1.name == name
    assert u1.age == age


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    try:
        test(conn)
    except Exception as e:
        print(repr(e))
    finally:
        conn.close()
