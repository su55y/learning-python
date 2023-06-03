from contextlib import contextmanager
import logging
from pathlib import Path
import sqlite3
from typing import List

from models import Entry


class Storage:
    def __init__(self, db_file: Path) -> None:
        self.db_file = db_file
        self.log = logging.getLogger()

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_file)
        try:
            yield conn.cursor()
        except Exception as e:
            self.log.error(e)
        else:
            conn.commit()
        finally:
            conn.close()

    def add_entries(self, entries: List[Entry]) -> int:
        if not entries:
            return 0
        with self.get_cursor() as cursor:
            query = (
                "INSERT OR IGNORE INTO tb_entries (id, title, updated) VALUES (?, ?, ?)"
            )
            self.log.debug(query)
            cursor.executemany(
                query,
                [(entry.id, entry.title, entry.updated) for entry in entries],
            )
            return cursor.rowcount
