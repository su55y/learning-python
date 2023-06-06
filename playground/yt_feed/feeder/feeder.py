import logging
from typing import Optional
import urllib.request


from models import Config, Entry, Feed
from parser import YTFeedParser
from storage import Storage


class Feeder:
    def __init__(self, config: Config, storage: Storage) -> None:
        self.stor = storage
        self.config = config
        self.log = logging.getLogger()

    def sync_channels(self):
        new_channels = self.stor.add_channels(self.config.channels)
        if new_channels:
            self.log.info(f"{new_channels} added")
        active_channels_ids = [(c.channel_id,) for c in self.config.channels]
        active_count = self.stor.sync_feeds(active_channels_ids)
        if active_count != len(self.config.channels):
            self.log.warning(
                "mismatch storage with config active channels: %d != %d"
                % (active_count, len(active_channels_ids)),
            )

    def sync_entries(self):
        for channel in self.config.channels:
            raw_feed = self._fetch_feed(channel.channel_id)
            if not raw_feed:
                self.log.warning("can't fetch feed for '%s'" % channel.title)
                continue
            parser = YTFeedParser(raw_feed)
            feed = Feed(
                channel_id=channel.channel_id,
                title=channel.title,
                is_active=True,
                entries=parser.entries,
            )
            count = self.stor.add_entries(feed)
            if count:
                self.log.info("%d new entries for '%s'" % (count, feed.title))

    def _fetch_feed(self, channel_id: str) -> Optional[str]:
        url = "https://www.youtube.com/feeds/videos.xml?channel_id=%s" % channel_id
        try:
            with urllib.request.urlopen(url) as resp:
                logging.debug(f"{resp.status} {resp.reason} {url}")
                if resp.status == 200:
                    return resp.read()
        except Exception as e:
            self.log.error("error: %s, url: %s" % (e, url))
