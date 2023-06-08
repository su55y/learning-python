from contextlib import contextmanager
import logging
from pathlib import Path
import sqlite3
from typing import List, Optional, Tuple

from models import Entry, Channel


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

    def sync_feeds(self, active_channels: List[Tuple[str]]):
        with self.get_cursor() as cursor:
            reset_query = "UPDATE tb_feeds SET is_active = 0"
            cursor.execute(reset_query)
            set_query = "UPDATE tb_feeds SET is_active = 1 WHERE channel_id = ?"
            return cursor.executemany(set_query, active_channels).rowcount

    def fetch_feed(self, channel_id: str) -> Optional[Channel]:
        with self.get_cursor() as cursor:
            query = "SELECT channel_id, title FROM tb_feeds WHERE channel_id = ?"
            self.log.debug(query)
            if feed_row := cursor.execute(query, (channel_id,)).fetchone():
                return Channel(*feed_row, entries=self.fetch_feed_entries(channel_id))

    def fetch_common_feed(self, limit=15) -> List[Entry]:
        entries: List[Entry] = []
        with self.get_cursor() as cursor:
            query = "SELECT id, title, updated FROM tb_entries ORDER BY UPDATED DESC LIMIT ?"
            self.log.debug(query)
            rows = cursor.execute(query, (limit,)).fetchall()
            for id, title, updated in rows:
                entries.append(Entry(id=id, title=title, updated=updated))
        return entries

    def fetch_feed_entries(self, channel_id: str) -> List[Entry]:
        entries: List[Entry] = []
        with self.get_cursor() as cursor:
            query = "SELECT id, title, updated FROM tb_entries WHERE channel_id = ?"
            self.log.debug(query)
            rows = cursor.execute(query, (channel_id,)).fetchall()
            for _id, title, updated in rows:
                entries.append(Entry(id=_id, title=title, updated=updated))
        return entries

    def add_channels(self, channels: List[Channel]) -> int:
        with self.get_cursor() as cursor:
            query = "INSERT OR IGNORE INTO tb_feeds (channel_id, title) VALUES (?, ?)"
            self.log.debug(query)
            return cursor.executemany(
                query, [(c.channel_id, c.title) for c in channels]
            ).rowcount

    def add_feed(self, feed: Channel) -> int:
        with self.get_cursor() as cursor:
            query = "INSERT OR IGNORE INTO tb_feeds (channel_id, title) VALUES (?, ?)"
            self.log.debug(query)
            return cursor.execute(query, (feed.channel_id, feed.title)).rowcount

    def add_entries(self, feed: Channel) -> int:
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
