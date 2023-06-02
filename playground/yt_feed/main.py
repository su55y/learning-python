from pathlib import Path
from sys import argv
from typing import Optional
import urllib.request

from storage import DBHooks, Storage
from parser import YTFeedParser

BASE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=%s"
DB_FILE = "test.db"


def fetch_feed(url: str) -> Optional[str]:
    try:
        with urllib.request.urlopen(url) as resp:
            if resp.status == 200:
                return resp.read()
    except:
        pass


if __name__ == "__main__":
    if len(argv[1:]) != 1:
        exit("provide channel id")

    channel_id = argv[1]
    raw_feed = fetch_feed(BASE_FEED_URL % channel_id)
    if not raw_feed:
        exit(f"can't fetch feed from {BASE_FEED_URL % channel_id}")

    parser = YTFeedParser(raw_feed)

    db_file = Path(DB_FILE)
    if err := DBHooks(db_file).init_db():
        exit(repr(err))

    storage = Storage(db_file)
    count = storage.add_entries(parser.entries)
    print(f"{count} new entries just added")
