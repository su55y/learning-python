from os import path
from threading import Thread
import time
from typing import IO

import asyncio

from utils import *


async def async_download(url: str) -> IO[bytes] | None:
    return await asyncio.to_thread(download_file, url)


async def process_file(name: str, url: str):
    if file := await async_download(url):
        Thread(target=extract, args=(file, path.join(PATH_TO_EXTRACT, name))).start()


async def main():
    tasks = [
        asyncio.create_task(process_file(name, url))
        for url in DOCS_URLS
        if (name := get_filename(url))
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    log.info(f"done in {time.perf_counter() - start:.2f}s")
