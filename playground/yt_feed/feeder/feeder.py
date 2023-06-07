import logging
from typing import Optional

import asyncio
from aiohttp import ClientSession

from models import Config, Feed, Channel
from parser import YTFeedParser
from storage import Storage


class Feeder:
    def __init__(self, config: Config, storage: Storage) -> None:
        self.stor = storage
        self.config = config
        self.log = logging.getLogger()

    def sync_channels(self) -> None:
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

    async def sync_entries(self) -> None:
        async with ClientSession() as session:
            await asyncio.gather(
                *[
                    asyncio.create_task(self._fetch_and_sync_entries(session, channel))
                    for channel in self.config.channels
                ]
            )

    async def _fetch_and_sync_entries(
        self, session: ClientSession, channel: Channel
    ) -> None:
        raw_feed = await self._fetch_feed(session, channel.channel_id)
        if not raw_feed:
            self.log.error("can't fetch feed for '%s'" % channel.title)
            return
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

    async def _fetch_feed(
        self, session: ClientSession, channel_id: str
    ) -> Optional[str]:
        url = "https://www.youtube.com/feeds/videos.xml?channel_id=%s" % channel_id
        async with session.get(url) as resp:
            self.log.debug(f"{resp.status} {resp.reason} {resp.url}")
            if resp.status == 200:
                return await resp.text()
