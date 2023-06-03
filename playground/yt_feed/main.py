import logging
from pathlib import Path
from sys import argv

from storage import DBHooks, Storage
from parser import YTFeedParser
from utils import fetch_feed

DB_FILE = "test.db"


def init_logger(**kwargs):
    LOG_FMT = "[%(asctime)-.19s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)"
    logger = logging.getLogger()
    logger.setLevel(kwargs.get("level", logging.INFO))

    if file := kwargs.get("file"):
        handler = logging.FileHandler(file)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter(kwargs.get("format", LOG_FMT)))
    logger.addHandler(handler)


if __name__ == "__main__":
    if len(argv[1:]) != 1:
        exit("provide channel id")

    init_logger()
    log = logging.getLogger()
    channel_id = argv[1]
    raw_feed = fetch_feed(channel_id)
    if not raw_feed:
        exit(f"can't fetch feed from {channel_id}")

    parser = YTFeedParser(raw_feed)
    feed = parser.parse_feed()

    db_file = Path(DB_FILE)
    if err := DBHooks(db_file).init_db():
        exit(repr(err))

    storage = Storage(db_file)
    count = storage.add_entries(feed.entries)
    log.info(f"{count} new entries just added")
