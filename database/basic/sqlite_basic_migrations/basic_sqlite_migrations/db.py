from importlib import resources
import logging
import sqlite3
import sys

import basic_sqlite_migrations.migrations as migrations_dir


def init_db(filepath: str) -> None:
    log = logging.getLogger()

    log.info(f"Connecting to {filepath!r}...")
    conn = sqlite3.connect(filepath)

    (current_version,) = next(conn.cursor().execute("PRAGMA user_version"), (0,))
    log.info(f"{current_version = }")

    migrations = list(resources.files(migrations_dir).iterdir())
    log.info(f"migrations = [{', '.join(f'{m.name!r}' for m in migrations)}]")

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
