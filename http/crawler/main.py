import argparse
import asyncio
import logging
from pathlib import Path

from httpx import AsyncClient

from crawler import Crawler

LOG_FMT = (
    "[%(asctime)s %(levelname)s] %(message)s (%(filename)s.%(funcName)s:%(lineno)d)"
)


def init_logger(file: Path = Path(__file__).parent.joinpath("crawler.log")) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(LOG_FMT))
    logger.addHandler(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="start url")
    return parser.parse_args()


async def run_crawler(url: str) -> None:
    async with AsyncClient() as client:
        crawler = Crawler(client, [url])
        await crawler.run()

    with open("urls.txt", "w") as f:
        for url in crawler.seen:
            print(url, file=f)


if __name__ == "__main__":
    init_logger()
    args = parse_args()
    asyncio.run(run_crawler(args.url))
