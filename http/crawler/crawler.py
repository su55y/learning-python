import asyncio
import logging
from typing import Optional, Set
import urllib.parse as urlparse

from httpx import AsyncClient

from parser import UrlParser


class Crawler:
    def __init__(
        self,
        client: AsyncClient,
        url: str,
        allowed_domains: Optional[Set[str]] = None,
    ) -> None:
        self.log = logging.getLogger()
        self.client = client
        self.queue = asyncio.Queue()
        self.seen = set()
        self.done = set()
        self.total = 0

        self.start_url = url
        self.allowed_domains = set([urlparse.urlparse(url).netloc])
        if url.startswith("www."):
            self.allowed_domains.add(url.lstrip("www."))
        if allowed_domains:
            self.allowed_domains.update(allowed_domains)

    async def run(self) -> None:
        self.log.info("run...")
        await self.on_found_links(set([self.start_url]))
        tasks = [asyncio.create_task(self.worker()) for _ in range(4)]
        await self.queue.join()

        for task in tasks:
            task.cancel()

    async def worker(self):
        while True:
            try:
                await self.process_one()
            except asyncio.CancelledError:
                return

    async def process_one(self):
        url = await self.queue.get()
        try:
            await self.crawl(url)
        except Exception as e:
            self.log.error(e)
        finally:
            self.queue.task_done()

    async def crawl(self, url: str):
        await asyncio.sleep(1)

        resp = await self.client.get(url, follow_redirects=True)
        self.log.debug("%s %s" % (resp.status_code, resp.reason_phrase))

        found_links = await self.parse_links(
            base=str(resp.url),
            text=resp.text,
        )

        await self.on_found_links(found_links)

        self.done.add(url)

    async def parse_links(self, base: str, text: str) -> Set[str]:
        parser = UrlParser(base, self.allowed_domains)
        parser.feed(text)
        return parser.found_links

    async def on_found_links(self, urls: Set[str]):
        self.seen.update(new := urls - self.seen)
        for url in new:
            await self.update_queue(url)

    async def update_queue(self, url: str):
        if self.total >= 8:
            return
        self.total += 1
        await self.queue.put(url)
