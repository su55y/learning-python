from typing import IO, Tuple
from io import BytesIO
from zipfile import ZipFile
from threading import Thread
from re import match
from os.path import join
from logging import basicConfig, INFO, info, error

import requests
import asyncio
import time


PATH_TO_EXTRACT = "python-docs"


def extract(b: IO[bytes], path: str) -> None:
    info(f"extracting file to {path}")
    try:
        ZipFile(b).extractall(path)
    except Exception as e:
        error(e)


async def async_download(url: str) -> IO[bytes] | None:
    return await asyncio.to_thread(download_file, url)


def download_file(url: str) -> IO[bytes] | None:
    info(f"donwloading file by {url}")
    resp = requests.get(url)
    if resp.status_code == 200:
        return BytesIO(resp.content)


async def process_file(name: str, url: str):
    file = await async_download(url)
    if not file:
        error(f"can't download file by {url}")
        return
    t = Thread(target=extract, args=(file, join(PATH_TO_EXTRACT, name)))
    t.start()


def init_logger():
    basicConfig(
        level=INFO,
        format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
        datefmt="%H:%M:%S %d/%m/%y",
    )


def parse_url(u: str) -> Tuple[str, bool]:
    if m := match(r"^https.+(docs\-.+)\.zip$", u):
        if (g := m.groups()) and len(g) == 1:
            return g[0], True
    return "", False


async def main():
    init_logger()
    docs_urls = [
        "https://docs.python.org/3/archives/python-3.11.1-docs-html.zip",
        "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-a4.zip",
        "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-letter.zip",
        "https://docs.python.org/3/archives/python-3.11.1-docs-text.zip",
    ]
    tasks = []
    for url in docs_urls:
        name, ok = parse_url(url)
        if not ok:
            continue
        tasks.append(asyncio.create_task(process_file(name, url)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    info(f"done in {time.perf_counter() - start:.2f}s")
