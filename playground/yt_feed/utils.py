import logging
from typing import Optional
import urllib.request


logger = logging.getLogger()

BASE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=%s"


def fetch_feed(channel_id: str) -> Optional[str]:
    url = BASE_FEED_URL % channel_id
    try:
        with urllib.request.urlopen(url) as resp:
            logging.debug(f"{resp.status} {resp.reason} {url}")
            if resp.status == 200:
                return resp.read()
    except Exception as e:
        logger.error(e)
