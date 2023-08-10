import argparse
import datetime as dt
import re
import subprocess
from typing import Optional, List, Dict

ffmpeg_cmd = """ffmpeg -hide_banner -loglevel warning -stats {y} {start} {to}
    -i {stream} {end} -c copy -avoid_negative_ts make_zero {output}"""


def parse_agrs() -> argparse.Namespace:
    rx_timestamp = re.compile(
        r"^(\d+|\d:[0-5]\d|[0-5]?\d:[0-5]\d|\d+:[0-5]\d:[0-5]\d)$"
    )

    def validate_url(url: str) -> Optional[str]:
        if not re.match(
            r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$",
            url,
        ):
            raise argparse.ArgumentTypeError("invalid url %r" % url)
        return url

    def validate_timestamp(timestamp: Optional[str] = None) -> Optional[str]:
        if timestamp is not None and not rx_timestamp.match(timestamp):
            raise argparse.ArgumentTypeError("invalid timestamp %r'" % timestamp)
        return timestamp

    def validate_resolution(resolution: str) -> Optional[str]:
        if not re.match(r"^\d{3,4}x\d{3,4}$", resolution):
            raise argparse.ArgumentTypeError(f"invalid resolution %r" % resolution)
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
        help="resolution of clip to download (default: %(default)s)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=f"clip{dt.datetime.now().strftime('%s')[-6:]}.mp4",
        metavar="PATH",
        help="path to output (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="overwrite output file if exists",
    )
    return parser.parse_args()


def get_stream_url(url: str, resolution: str) -> str:
    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        exit(f"{e}\nhttps://github.com/yt-dlp/yt-dlp#installation")

    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        if not info or not isinstance(info, Dict):
            exit("can't extract info by url %r" % url)

        if len(streams := info.get("formats", [])) == 0:
            exit("no streams present by url %r" % url)
        for format in streams:
            if not format.get("vcodec") or not format.get("acodec"):
                continue

            if format.get("resolution") == resolution:
                if not re.match(r"^https.+", url := format.pop("url")):
                    exit("can't get stream url from format: %s" % format)
                print("choosed format: %s" % format)
                return url
    exit("can't find stream by url %r" % url)


def build_cmd(args: argparse.Namespace) -> List[str]:
    return ffmpeg_cmd.format(
        y="-y" if args.force else "",
        start="-ss %s" % (args.start or 0),
        to="-to %s" % args.to if args.to else "",
        stream=get_stream_url(args.url, args.resolution),
        end="-t %s" % args.duration if args.duration else "",
        output=args.output,
    ).split()


if __name__ == "__main__":
    subprocess.run(build_cmd(parse_agrs()))
