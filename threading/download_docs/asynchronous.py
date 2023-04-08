from io import BytesIO
import logging
from os import path
import re
from threading import Thread
import time
from typing import IO
from zipfile import ZipFile

import asyncio
import requests


PATH_TO_EXTRACT = "python-docs"
LOG_FMT = "\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s"

log: logging.Logger
rx_docs_url = re.compile(r"/([^/]+\.[^/]+)$")
docs_urls = [
    "https://docs.python.org/3/archives/python-3.11.1-docs-html.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-a4.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-letter.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-text.zip",
]


def extract(b: IO[bytes], path: str) -> None:
    log.info(f"extracting file to {path}")
    try:
        ZipFile(b).extractall(path)
    except Exception as e:
        log.error(e)


async def async_download(url: str) -> IO[bytes] | None:
    return await asyncio.to_thread(download_file, url)


def download_file(url: str) -> IO[bytes] | None:
    log.info(f"donwloading file by {url}")
    if (resp := requests.get(url)) and resp.status_code == 200:
        return BytesIO(resp.content)


async def process_file(name: str, url: str):
    if not (file := await async_download(url)):
        log.error(f"can't download file by {url}")
        return
    t = Thread(target=extract, args=(file, path.join(PATH_TO_EXTRACT, name)))
    t.start()


def init_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT, "%H:%M:%S %d/%m/%y"))
    log.addHandler(sh)


def get_filename(u: str) -> str | None:
    if (match := rx_docs_url.findall(u)) and len(match) == 1:
        return match.pop()


async def main():
    tasks = [
        asyncio.create_task(process_file(name, url))
        for url in docs_urls
        if (name := get_filename(url))
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    init_logger()
    start = time.perf_counter()
    asyncio.run(main())
    log.info(f"done in {time.perf_counter() - start:.2f}s")
