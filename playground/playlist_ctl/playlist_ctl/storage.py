from contextlib import contextmanager
import logging
from pathlib import Path
import sqlite3
from typing import Dict, Literal, Optional, Tuple, Union


class Storage:
    def __init__(self, file: Union[Path, Literal[":memory:"]] = ":memory:") -> None:
        self.file = file
        if isinstance(self.file, Path) and not self.file.parent.exists():
            self.file.parent.mkdir(parents=True)

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.file)
        try:
            cursor = conn.cursor()
            yield cursor
        except Exception as e:
            logging.critical(e)
        else:
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> Optional[Exception]:
        titles_schema = """CREATE TABLE IF NOT EXISTS titles (
        url TEXT PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        created DATETIME NOT NULL)"""
        try:
            with self.get_cursor() as cur:
                cur.execute(titles_schema)
        except Exception as e:
            return e

    def insert_title(self, title: Tuple[str, str, str]) -> Optional[Exception]:
        query = "INSERT OR IGNORE INTO titles (url, title, created) VALUES (?, ?, ?)"
        try:
            with self.get_cursor() as cur:
                logging.debug("%s: %s" % (query, title))
                cur.execute(query, title)
        except Exception as e:
            logging.error(e)
            return e

    def select_title(self, url: str) -> Optional[str]:
        try:
            with self.get_cursor() as cur:
                cur.execute("SELECT title FROM titles WHERE url = ? LIMIT 1", (url,))
                title, *_ = row if (row := cur.fetchone()) else (None,)
                return title
        except Exception as e:
            logging.error(e)

    def select_titles(self, urls: str) -> Dict[str, str]:
        try:
            with self.get_cursor() as cur:
                q = "SELECT url, title FROM titles WHERE url in (%s)" % urls
                logging.debug(q)
                cur.execute(q)
                return {url: title for url, title in cur.fetchall()}
        except Exception as e:
            logging.error("can't select titles: %s" % e)
            return {}
