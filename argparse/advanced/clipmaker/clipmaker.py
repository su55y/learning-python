import argparse
import re
import subprocess
from typing import Optional, List, Dict


def parse_agrs() -> argparse.Namespace:
    def validate_url(url: str) -> Optional[str]:
        if not re.match(
            r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$",
            url,
        ):
            raise argparse.ArgumentTypeError("invalid url")
        return url

    def validate_timestamp(timestamp: Optional[str] = None) -> Optional[str]:
        if timestamp is not None and not re.match(
            r"(^[0-9]\:[0-5][0-9]$)|(^[0-5]?[0-9]\:[0-5][0-9]$)|(^[0-9]{1,2}\:[0-5][0-9]\:[0-5][0-9]$)|(^[0-5]?[0-9]$)",
            timestamp,
        ):
            raise argparse.ArgumentTypeError(f"invalid timestamp '{timestamp}'")
        return timestamp

    def validate_resolution(resolution: str) -> Optional[str]:
        if not re.match(r"^\d{3,4}x\d{3,4}$", resolution):
            raise argparse.ArgumentTypeError(f"invalid resolution '{resolution}'")
        return resolution

    parser = argparse.ArgumentParser(
        prog="clipmaker",
        description="Download clips from YouTube or Twitch",
    )
    parser.add_argument("url", type=validate_url, metavar="URL")
    parser.add_argument(
        "-s",
        "--start",
        type=validate_timestamp,
        metavar="T",
        help="clip start time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=validate_timestamp,
        metavar="T",
        help="clip duration (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-t",
        "--to",
        type=validate_timestamp,
        metavar="T",
        help="clip stop time (59/9:59/9:59:59)",
    )
    parser.add_argument(
        "-r",
        "--resolution",
        type=validate_resolution,
        default="1280x720",
        help="resolution of clip to download (default %(default)s)",
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
    )
    return parser.parse_args()


def get_stream_url(url: str, resolution: str) -> Optional[str]:
    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        exit(f"{e}\nhttps://github.com/yt-dlp/yt-dlp#installation")

    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        if not info or not isinstance(info, Dict):
            exit(f"can't extract info by '{url}'")

        for format in info.get("formats", []):
            if (
                format.get("vcodec", "none") == "none"
                or format.get("acodec", "none") == "none"
            ):
                continue
            if format.get("resolution") == resolution:
                url = format.get("url", "")
                if not re.match(r"^https.+", url):
                    exit("can't get valid stream url")
                return url
        print("can't find stream, try other resolution")


def build_cmd(args: argparse.Namespace) -> List[str]:
    start = "-ss %s" % (args.start or 0)
    y = "-y" if args.force else ""
    to = f"-to {args.to}" if args.to else ""
    end = f"-t {args.duration}" if args.duration else ""
    stream = get_stream_url(args.url, args.resolution)
    if not stream:
        exit(1)

    return (
        f"""ffmpeg -hide_banner -loglevel warning -stats {y} 
            {start} -i {stream} {to} {end} -c copy -avoid_negative_ts make_zero {args.output}"""
    ).split()


if __name__ == "__main__":
    subprocess.run(build_cmd(parse_agrs()))
