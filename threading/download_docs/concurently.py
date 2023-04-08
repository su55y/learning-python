from os import path
import time
from threading import Thread


from utils.utils import (
    log,
    extract,
    download_file,
    get_filename,
    DOCS_URLS,
    PATH_TO_EXTRACT,
)


def process_file(name: str, url: str):
    if file := download_file(url):
        extract(file, path.join(PATH_TO_EXTRACT, name))


def main():
    thread_list = list()
    for url in DOCS_URLS:
        if name := get_filename(url):
            t = Thread(
                target=process_file,
                args=(name, url),
                name=f"process_file({name})",
            )
            log.info(f"starting new thread {t.name}")
            thread_list.append(t)
            t.start()
    for t in thread_list:
        t.join()


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    log.info(f"done in {time.perf_counter() - start:.2f}s")
