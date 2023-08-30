import argparse
import asyncio
import logging
from pathlib import Path

from httpx import AsyncClient

from crawler import Crawler

LOG_FMT = "[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)"


def init_logger(file: Path = Path(__file__).parent.joinpath("crawler.log")) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(LOG_FMT))
    logger.addHandler(fh)


def parse_args() -> argparse.Namespace:
    ...


async def run_crawler() -> None:
    async with AsyncClient() as client:
        crawler = Crawler(client, [])
        await crawler.run()


if __name__ == "__main__":
    init_logger()
    asyncio.run(run_crawler())
