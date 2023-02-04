from typing import IO, List, Tuple
from requests import get
from io import BytesIO
from zipfile import ZipFile
from os.path import join
from logging import basicConfig, INFO, info, error
from re import match


PATH_TO_EXTRACT = "python-docs"


def extract(b: IO[bytes], path: str) -> Exception | None:
    info(f"extracting file to {path}")
    try:
        ZipFile(b).extractall(path)
    except Exception as e:
        return e


def download_file(url: str) -> IO[bytes] | None:
    info(f"donwloading file by {url}")
    r = get(url)
    if r.status_code == 200:
        return BytesIO(r.content)


def process_file(name: str, url: str):
    file = download_file(url)
    if not file:
        error(f"can't download file by {url}")
        return
    if e := extract(file, join(PATH_TO_EXTRACT, name)):
        error(f"can't extract '{name}' due to error: {repr(e)}")


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


def main():
    init_logger()
    docs_urls: List[str] = list(
        [
            "https://docs.python.org/3/archives/python-3.11.1-docs-html.zip",
            "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-a4.zip",
            "https://docs.python.org/3/archives/python-3.11.1-docs-pdf-letter.zip",
            "https://docs.python.org/3/archives/python-3.11.1-docs-text.zip",
        ]
    )

    for url in docs_urls:
        name, ok = parse_url(url)
        if not ok:
            info(f"can't parse url {url}")
            continue
        info(f"processing file {name}")
        process_file(name, url)


if __name__ == "__main__":
    main()
