#!/usr/bin/env -S python3 -u

from sys import exit, argv
from typing import Tuple
from re import match
from textwrap import dedent
from os.path import isfile
from yt_dlp import YoutubeDL


def print_help():
    print(
        dedent(
            """
            progname [url] [output] [-h]

            arguments:
                output  /path/to/file
                url URL
                -h, --help, -?  show this message

          """
        )
    )


def parse_agrs() -> Tuple[str, str, bool]:
    url, output, force = None, None, False
    url_re = r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})"

    for v in argv[1:]:
        if match(url_re, v) and not url:
            url = v
        if match(r"^[\w\d\-_\s\/]+$", v) and not output:
            output = v
        if match(r"^(-h|--help)$", v):
            print_help()
            exit(0)
        if match(r"^(-f|--force)$", v):
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

    with YoutubeDL(
        {
            "outtmpl": f"{output}.%(ext)s",
            "format": "best[ext=mp4]/best",
        }
    ) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    main()
