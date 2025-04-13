snippet used in [basic_sqlite_migrations/db.py](basic_sqlite_migrations/db.py) source: [_eskerda's_ blog](https://eskerda.com/sqlite-schema-migrations-python/)

```python
import os
import sys
import sqlite3
import logging

log = logging.getlogger("foo")

DB_URI = os.getenv("DB_URI", "foo.db")
conn = sqlite3.connect(db_uri)

current_version, = next(conn.cursor().execute('PRAGMA user_version'), (0, ))

migrations = resources.files('migrations').iterdir()

for migration in migrations[current_version:]:
    cur = conn.cursor()
    try:
        log.info("Applying %s", migration.name)
        cur.executescript("begin;" + migration.read_text())
    except Exception as e:
        log.error("Failed migration %s: %s. Bye", migration.name, e)
        cur.execute("rollback")
        sys.exit(1)
    else:
        cur.execute("commit")
```
