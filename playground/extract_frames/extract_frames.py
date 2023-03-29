import argparse
import json
import re
import subprocess
import os.path
from pathlib import Path

EXTRACT_CMD = "ffmpeg -i %s -vf thumbnail=%s,setpts=N/TB -r 1 -vframes %d %s"
PROBE_CMD = "ffprobe -v quiet -show_streams -select_streams v:0 -of json %s"


def parse_args():
    def check_num(arg: str) -> int | None:
        try:
            num = int(arg)
        except:
            raise argparse.ArgumentTypeError(f"invalid number '{arg}'")
        else:
            return num

    def check_file(arg: str) -> str | None:
        if not os.path.exists(arg) or not os.path.isfile(arg):
            raise argparse.ArgumentTypeError(f"invalid file path '{arg}'")
        return arg

    def check_format(arg: str) -> Path | None:
        try:
            path = Path(arg)
            if not re.match(r"^.+%(?:0\d)?d\..+$", path.name):
                raise argparse.ArgumentTypeError(f"invalid format '{path.name}'")
            if not path.parent.exists():
                exit(0) if not re.match(
                    r"^[yY](?:es)?$",
                    input(
                        f"path '{path.parent.absolute()}' not exists, create?\n[y/n (default: n)]: "
                    ),
                ) else path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise argparse.ArgumentTypeError(f"parse format error: {e}")
        else:
            return path

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        type=check_file,
        metavar="PATH",
        help="input file",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=check_num,
        default=10,
        metavar="INT",
        help="frames count (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=check_format,
        default="frames/frame%d.png",
        metavar="STRING",
        help="output format (default: %(default)s), should include %%d format specifier",
    )

    return parser.parse_args()


def get_interval(file: str, framecount: int) -> float | bool:
    rx_fps = re.compile(r"(\d+(?:\.\d+)?)\/1")
    rx_duration = re.compile(r"(\d+(?:\.\d+)?)")

    try:
        probe = json.loads(
            subprocess.check_output(PROBE_CMD % file, shell=True).decode()
        )
        match probe:
            case {"streams": [{"r_frame_rate": str(), "duration": str()}]}:
                fps_str = probe["streams"][0]["r_frame_rate"]
                duration_str = probe["streams"][0]["duration"]
                if (
                    (duration := rx_duration.findall(duration_str).pop()) and
                    (fps := rx_fps.findall(fps_str).pop())
                ):
                    return round((float(fps) * float(duration)) / framecount, 2)
    except Exception as e:
        if isinstance(e, IndexError):
            print(f"unexpected probe format")
        else:
            print(repr(e))
    return False


if __name__ == "__main__":
    args = parse_args()
    if interval := get_interval(args.file, args.count):
        subprocess.run((EXTRACT_CMD % (args.file, interval, args.count, args.format,)).split())
