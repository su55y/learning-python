from contextlib import contextmanager
import logging
from pathlib import Path
import sqlite3
from typing import List, Optional

from models import Feed, Entry


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

    def fetch_feed(self, channel_id: str) -> Optional[Feed]:
        with self.get_cursor() as cursor:
            query = "SELECT channel_id, title FROM tb_feeds WHERE channel_id = ?"
            self.log.debug(query)
            if feed_row := cursor.execute(query, (channel_id,)).fetchone():
                _channel_id, title = feed_row
                return Feed(
                    channel_id=_channel_id,
                    title=title,
                    entries=self.fetch_feed_entries(channel_id),
                )

    def fetch_feed_entries(self, channel_id: str) -> List[Entry]:
        entries: List[Entry] = []
        with self.get_cursor() as cursor:
            query = "SELECT id, title, updated FROM tb_entries WHERE channel_id = ?"
            self.log.debug(query)
            rows = cursor.execute(query, (channel_id,)).fetchall()
            for _id, title, updated in rows:
                entries.append(Entry(id=_id, title=title, updated=updated))
        return entries

    def add_feed(self, feed: Feed) -> int:
        with self.get_cursor() as cursor:
            query = "INSERT INTO tb_feeds (channel_id, title) VALUES (?, ?)"
            self.log.debug(query)
            return cursor.execute(query, (feed.channel_id, feed.title)).rowcount

    def add_entries(self, feed: Feed) -> int:
        if not feed.entries:
            return 0
        with self.get_cursor() as cursor:
            query = "INSERT OR IGNORE INTO tb_entries (id, title, updated, channel_id) VALUES (?, ?, ?, ?)"
            entries = [
                (entry.id, entry.title, entry.updated, feed.channel_id)
                for entry in feed.entries
            ]
            self.log.debug(f"{query}, entries count: {len(entries)}")
            return cursor.executemany(query, entries).rowcount
