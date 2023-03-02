#!/usr/bin/env -S python3 -u

from os.path import isfile
import re
from sys import exit, argv
from typing import Tuple


HELP_MSG = """dlvid URL OUTPUT [-h] [-f]
arguments:
    URL             : youtube video url
    OUTPUT          : /path/to/file (without extension)
    -f, --force     : overwrite file if exists
    -h, --help, -?  : show this message
"""

rx_help = re.compile(r"^(-h|--help)$")
rx_force = re.compile(r"^(-f|--force)$")
rx_path = re.compile(r"^[\w\d\-_\s\/]+$")
rx_url = re.compile(
    r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})"
)


def parse_agrs() -> Tuple[str, str, bool]:
    url, output, force = None, None, False

    for v in argv[1:]:
        if rx_help.match(v):
            print(HELP_MSG)
            exit(0)
        if rx_url.match(v) and not url:
            url = v
        if rx_path.match(v) and not output:
            output = v
        if re.match(r"^(-f|--force)$", v):
            force = True

    if not url:
        print("invalid url")
        exit(1)
    if not output:
        print("invalid output")
        exit(1)

    return url, output, force


def main():
    url, output, force = parse_agrs()

    if isfile(f"{output}.mp4") and not force:
        print(f"file '{output}.mp4' already exists")
        exit(1)

    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        print(f"{repr(e)}\nhttps://github.com/yt-dlp/yt-dlp#installation")
        exit(1)

    with YoutubeDL(
        {
            "outtmpl": f"{output}.%(ext)s",
            "format": "best[ext=mp4]/best",
            "overwrites": force,
        }
    ) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    main()
