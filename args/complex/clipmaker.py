#!/usr/bin/env -S python3 -u

from argparse import ArgumentParser, Namespace
import logging
import re
import subprocess
from typing import Tuple

from config import LOG_LEVEL, LOG_FMT, RESOLUTION


log: logging.Logger

rx_timestamp = re.compile(
    r"(^[0-9]\:[0-5][0-9]$)|(^[0-5]?[0-9]\:[0-5][0-9]$)|(^[0-9]{1,2}\:[0-5][0-9]\:[0-5][0-9]$)|(^[0-5]?[0-9]$)"
)
rx_url = re.compile(
    r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$"
)


def init_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(LOG_FMT))
    log.addHandler(sh)


def die(msg: str):
    log.error(msg)
    exit(1)


def parse_agrs() -> Namespace:
    parser = ArgumentParser(
        prog="clipmaker",
        description="Download clips from YouTube or Twitch",
    )
    parser.add_argument("default", metavar="URL", help="url")
    parser.add_argument(
        "-s",
        "--start",
        metavar="T",
        help="clip start time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        metavar="T",
        help="clip duration (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-t",
        "--to",
        metavar="T",
        help="clip stop time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help="path to output",
        default="out.mp4",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite output file if exists",
        default=False,
    )
    return parser.parse_args()


def get_va(url: str) -> Tuple[str, str]:
    if not re.match(r"^\d{3,4}x\d{3,4}$", RESOLUTION):
        die(f"invalid resolution: '{RESOLUTION}'")
    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        die(f"{repr(e)}\nhttps://github.com/yt-dlp/yt-dlp#installation")

    audio, video = None, None
    with YoutubeDL({"format": "best[ext=mp4]+bestaudio"}) as ydl:
        info = ydl.extract_info(url, download=False)
        for format in info["formats"]:
            if (
                format.get("resolution") == "audio only" and format.get("ext") == "m4a"
            ) or (
                format.get("resolution") == "audio only" and format.get("ext") == "mp4"
            ):
                audio = format
            if (
                (format.get("resolution") == RESOLUTION and format.get("ext") == "mp4")
                or (format.get("resolution") == RESOLUTION.split("x").pop() + "p60")
                or (format.get("resolution") == RESOLUTION.split("x").pop() + "p")
            ):
                video = format

    if not video or not audio:
        die(f"video or audio object is None: ('{video}', '{audio}')")

    v, a = video.get("url"), audio.get("url")
    if not all(re.match(r"^https.+$", u) for u in [v, a]):
        die(f"invalid stream url: ('{v}', {a})")

    return v, a


def build_cmd(args: Namespace) -> list[str]:
    if not args.default or not rx_url.match(args.default):
        die(f"invalid url '{args.default}'")

    start = "-ss 0"
    if args.start and rx_timestamp.match(args.start):
        start = f"-ss {args.start}"

    end = to = ""
    if args.to and rx_timestamp.match(args.to):
        to = f"-to {args.to}"
    elif args.duration and rx_timestamp.match(args.duration):
        end = f"-t {args.duration}"

    y = ""
    if args.force:
        y = "-y"

    v, a = get_va(args.default)

    return (
        f"""ffmpeg -hide_banner -loglevel warning -stats {y} {start} {to} -i {v}
            {start} {to} -i {a} {end}
            -map 0:v -map 1:a -c:v libx264 -c:a aac {args.output}"""
    ).split()


def main():
    try:
        args = parse_agrs()
    except Exception as e:
        die(repr(e))

    log.info(
        ", ".join(
            [f"{k}={v}" for k, v in vars(args).items() if not k.startswith("__")],
        )
    )
    p = subprocess.Popen(build_cmd(args))
    log.info(f"status: {p.wait()}")


if __name__ == "__main__":
    init_logger()
    main()
