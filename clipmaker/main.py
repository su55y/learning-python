#!/usr/bin/env -S python3 -u

from argparse import ArgumentParser, Namespace
from re import match
from subprocess import run
from typing import Tuple

from yt_dlp import YoutubeDL
from utils.custom_logger import CustomLogger
from config import LOGLEVEL, RESOLUTION

log = CustomLogger(__name__, LOGLEVEL)


def die(msg: str):
    log.error(msg)
    exit(1)


def parse_agrs() -> Namespace:
    parser = ArgumentParser(
        prog="clipmaker",
        description="Download clips from youtube of twitch",
    )
    parser.add_argument("default", metavar="URL", help="url")
    parser.add_argument(
        "-s",
        "--start",
        action="store",
        type=str,
        metavar="T",
        help="clip start time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        action="store",
        type=str,
        metavar="T",
        help="clip duration (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-t",
        "--to",
        action="store",
        type=str,
        metavar="T",
        help="clip stop time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
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


def validate_time_arg(s: str) -> bool:
    for r in [
        r"^[0-9]\:[0-5][0-9]$",
        r"^[0-5]?[0-9]\:[0-5][0-9]$",
        r"^[0-9]{1,2}\:[0-5][0-9]\:[0-5][0-9]$",
        r"^\d{1,5}$",
    ]:
        if match(r, s):
            return True

    log.warning(f"invalid time '{s}'")
    return False


def get_va(url: str) -> Tuple[str, str]:
    if not match(r"^\d{3,4}x\d{3,4}$", RESOLUTION):
        die(f"invalid resolution: '{RESOLUTION}'")

    audio, video = None, None
    with YoutubeDL({"format": "best[ext=mp4]+bestaudio"}) as ydl:
        info = ydl.extract_info(url, download=False)
        for _, format in enumerate(info["formats"]):
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
    if not all(match(r"^https.+$", u) for u in [v, a]):
        die(f"invalid stream url: ('{v}', {a})")

    return v, a


def build_cmd(args: Namespace) -> list[str]:
    if not args.default or not match(
        r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$",
        args.default,
    ):
        die(f"invalid url '{args.default}'")

    start = "-ss 0"
    if args.start and validate_time_arg(args.start):
        start = f"-ss {args.start}"

    end, to = "", ""
    if args.to and validate_time_arg(args.to):
        to = f"-to {args.to}"
    elif args.duration and validate_time_arg(args.duration):
        end = f"-t {args.duration}"

    y = ""
    if args.force:
        y = "-y"

    v, a = get_va(args.default)

    return (
        f"""ffmpeg {y} {start} {to} -i {v}
            {start} {to} -i {a} {end}
            -map 0:v -map 1:a -c:v libx264 -c:a aac {args.output}"""
    ).split()


def main():
    try:
        args = parse_agrs()
    except Exception as e:
        die(repr(e))

    log.info(args)
    log.info(run(build_cmd(args)))


if __name__ == "__main__":
    main()
