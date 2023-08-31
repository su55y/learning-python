import argparse
import asyncio
import logging
from pathlib import Path
from typing import Set
import urllib.parse as urlparse

from httpx import AsyncClient

from crawler import Crawler

LOG_FMT = (
    "[%(asctime)s %(levelname)s] %(message)s (%(filename)s.%(funcName)s:%(lineno)d)"
)


def init_logger(file: Path) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file)
    fh.setFormatter(logging.Formatter(LOG_FMT))
    logger.addHandler(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="start url")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output file (default: 'url_domain.txt')",
    )
    parser.add_argument("-l", "--log-file", type=Path, help="log file")
    return parser.parse_args()


def write_results(file: Path, results: Set[str]) -> None:
    sorted_results = sorted(results)
    with open(file, "w") as f:
        for u in sorted_results:
            print(u, file=f)
    print("%d entries are made to the %s" % (len(sorted_results), file))


async def main(args: argparse.Namespace) -> None:
    async with AsyncClient() as client:
        crawler = Crawler(client, args.url)
        await crawler.run()
        write_results(
            args.output
            if args.output
            else Path("%s.txt" % urlparse.urlparse(args.url).netloc),
            crawler.seen,
        )


if __name__ == "__main__":
    args = parse_args()
    if args.log_file:
        init_logger(args.log_file)
    asyncio.run(main(args))
