import argparse
import datetime as dt
import re
import subprocess
from typing import Optional, Dict

ffmpeg_cmd = """ffmpeg -hide_banner -loglevel warning -stats {y} {start} {to}
    -i {stream} {end} -c copy -avoid_negative_ts make_zero {output}"""
filters = {"ext": "mhtml", "filesize": None, "format_note": "storyboard"}


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
    parser.add_argument("-c", "--choose", action="store_true", help="choose format")
    return parser.parse_args()


def filter_formats(f: Dict) -> bool:
    for k, v in filters.items():
        if f.get(k) == v:
            return False
    return True


def choose_format(url: str, resolution: str, choose: bool) -> str:
    try:
        from yt_dlp import YoutubeDL
    except ImportError as e:
        exit(f"{e}\nhttps://github.com/yt-dlp/yt-dlp#installation")

    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        if not info or not isinstance(info, Dict):
            exit("can't extract info")
        if not info.get("formats"):
            exit("can't get formats from info")
        info["formats"] = filter(filter_formats, info["formats"])
        formats_map = {f["format_id"]: f for f in info["formats"]}
        if choose:
            print(ydl.render_formats_table({**info, "formats": formats_map.values()}))
            while True:
                choice = input("format id: ")
                if format := formats_map.get(choice):
                    return format["url"]
                print("not found format %r" % choice)
        else:
            for f in formats_map.values():
                if not f.get("vcodec") or not f.get("acodec"):
                    continue
                if f.get("resolution") == resolution:
                    if not re.match(r"^https.+", url := f.pop("url")):
                        exit("can't get stream url from format: %s" % f)
                    print("choosed format: %s" % f)
                    return url
            exit("resolution %r not available" % resolution)


if __name__ == "__main__":
    args = parse_agrs()
    url = choose_format(args.url, args.resolution, args.choose)
    subprocess.run(
        ffmpeg_cmd.format(
            y="-y" if args.force else "",
            start="-ss %s" % (args.start or 0),
            to="-to %s" % args.to if args.to else "",
            stream=url,
            end="-t %s" % args.duration if args.duration else "",
            output=args.output,
        ).split()
    )
