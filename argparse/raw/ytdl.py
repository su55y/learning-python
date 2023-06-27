from dataclasses import dataclass
import re
import sys
from typing import Optional

HELP_MSG = """ytdl.py [-h] [-o PATH] [-f] URL

positional arguments:
    URL                 youtube video url

options:
    -o, --output PATH   output path (default: %(title)s.%(ext)s)
    -f, --force         overwrite file if exists
    -h, --help          show this message
"""


@dataclass
class Args:
    url: str
    output: Optional[str] = None
    force: bool = False


def parse_agrs():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(HELP_MSG)
        exit(0)

    output = url = None
    for i, arg in enumerate(args):
        match arg:
            case "-o" | "--output":
                if len(args) < i + 2:
                    exit("can't reach output value")
                output = args.pop(i + 1)
            case _:
                if not re.match(
                    r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})",
                    arg,
                ):
                    exit("invalid url '%s'" % arg)
                url = arg
    if not url:
        exit("URL is reguired")
    force = "-f" in args or "--force" in args
    return Args(url=url, output=output, force=force)


if __name__ == "__main__":
    args = parse_agrs()
    params = {
        "format": "best[ext=mp4]/best",
        "outtmpl": args.output or "%(title)s.%(ext)s",
        "overwrites": args.force,
    }
    try:
        from yt_dlp import YoutubeDL

        with YoutubeDL(params) as ydl:
            ydl.download([args.url])
    except ImportError as e:
        exit(f"{e}\nhttps://github.com/yt-dlp/yt-dlp#installation")
    except Exception as e:
        exit(str(e))
