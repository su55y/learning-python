from os import path
import time
import threading

from utils import *


def process_file(name: str, url: str):
    if file := download_file(url):
        extract(file, path.join(PATH_TO_EXTRACT, name))


def main():
    for url in DOCS_URLS:
        if name := get_filename(url):
            t = threading.Thread(
                target=process_file,
                args=(name, url),
                name=f"process_file({name})",
            )
            log.info(f"starting new thread {t.name}")
            t.start()

    while True:
        if any(
            t.is_alive()
            for t in threading.enumerate()
            if t.name.startswith("process_file")
        ):
            time.sleep(0.1)
            continue
        break


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    log.info(f"done in {time.perf_counter() - start:.2f}s")
