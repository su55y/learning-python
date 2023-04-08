from io import BytesIO
import logging
import re
from typing import IO
from zipfile import ZipFile

import requests

PATH_TO_EXTRACT = "python-docs"
LOG_FMT = "\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s"
LOG_DATE_FMT = "%H:%M:%S %d/%m/%y"
DOCS_URLS = [
    "https://docs.python.org/3/archives/python-3.11.1-docs-html.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-a4.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-letter.zip",
    "https://docs.python.org/3/archives/python-3.11.1-docs-text.zip",
]

rx_docs_url = re.compile(r"/([^/]+\.[^/]+)$")


def get_filename(url: str) -> str | None:
    if (match := rx_docs_url.findall(url)) and len(match) == 1:
        return match.pop()
    log.error(f"can't get filename from {url}")


def download_file(url: str) -> IO[bytes] | None:
    log.info(f"donwloading file by {url}")
    if (resp := requests.get(url)) and resp.status_code == 200:
        return BytesIO(resp.content)
    log.warning(f"({resp.status_code} {resp.reason}) can't download file by {url}")


def extract(b: IO[bytes], path: str) -> None:
    log.info(f"extracting file to {path}")
    try:
        ZipFile(b).extractall(path)
    except Exception as e:
        log.error(f"can't extract to '{path}' due to error: {e}")


def init_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT, LOG_DATE_FMT))
    log.addHandler(sh)
    return log


log = init_logger()
