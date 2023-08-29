import asyncio
import logging
from pathlib import Path

from httpx import AsyncClient

from .crawler import Crawler

LOG_FMT = "[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)"


def init_logger(file: Path = Path(__file__).parent.joinpath("crawler.log")) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(LOG_FMT))
    logger.addHandler(fh)


async def run_crawler():
    async with AsyncClient() as client:
        crawler = Crawler(client)
        await crawler.run()


if __name__ == "__main__":
    asyncio.run(run_crawler())
