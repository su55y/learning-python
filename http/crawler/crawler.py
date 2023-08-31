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
        limit: int = 100,
        routines_count: int = 10,
        ratelimit: float = 1,
    ) -> None:
        self.log = logging.getLogger()
        self.client = client
        self.queue = asyncio.Queue()
        self.seen = set()
        self.done = set()
        self.total = 0
        self.limit = limit
        self.routines_count = routines_count
        self.ratelimit = ratelimit

        self.start_url = url
        self.allowed_domains = set([urlparse.urlparse(url).netloc])
        if url.startswith("www."):
            self.allowed_domains.add(url.lstrip("www."))
        if allowed_domains:
            self.allowed_domains.update(allowed_domains)

    async def run(self) -> None:
        self.log.info("run...")
        await self.on_found_links(set([self.start_url]))
        tasks = [asyncio.create_task(self.worker()) for _ in range(self.routines_count)]
        await self.queue.join()

        for task in tasks:
            task.cancel()

    async def worker(self) -> None:
        while True:
            try:
                await self.process_one()
            except asyncio.CancelledError:
                return

    async def process_one(self) -> None:
        url = await self.queue.get()
        try:
            await self.crawl(url)
        except Exception as e:
            self.log.error(e)
        finally:
            self.queue.task_done()

    async def crawl(self, url: str) -> None:
        await asyncio.sleep(self.ratelimit)
        resp = await self.client.get(url, follow_redirects=True)
        self.log.debug("%s %s %s" % (resp.status_code, resp.reason_phrase, resp.url))
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

    async def on_found_links(self, urls: Set[str]) -> None:
        self.seen.update(new := urls - self.seen)
        for url in new:
            await self.update_queue(url)

    async def update_queue(self, url: str) -> None:
        if self.total >= self.limit:
            return
        self.total += 1
        await self.queue.put(url)
