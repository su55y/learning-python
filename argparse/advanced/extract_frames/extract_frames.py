import argparse
from dataclasses import dataclass
import json
import math
import re
import subprocess as sp
import os.path
from pathlib import Path
from sys import argv

FFMPEG = "ffmpeg"
FFPROBE = "ffprobe"
MONTAGE = "montage"

OVERWITE = "-y" in argv[1:]

EXTRACT_CMD = f"{FFMPEG} %s -i %s -vf thumbnail=%s,setpts=N/TB -r 1 -vframes %d %s"
SILENCE_OPTS = "-hide_banner -loglevel warning -stats"
PROBE_CMD = f"{FFPROBE} -v quiet -show_streams -select_streams v:0 -of json %s"
MOTAGE_CMD = f"{MONTAGE} -geometry +0+0 -tile %s %s %s"

DEFAULT_COUNT = 10
DEFAULT_FMT = "frames/frame%02d.png"
DEFAULT_PREVIEW = "preview.png"

MKDIR_MSG = "path '%s' not exists, create?\n[y/n (default: n)]: "


rx_num = re.compile(r"(\d+)")
rx_fmt = re.compile(r"^.+%(?:0\d)?d\..+$")
rx_yes = re.compile(r"^[yY](?:es)?$")
rx_fps = re.compile(r"(\d+(?:\.\d+)?)\/1")
rx_dur = re.compile(r"(\d+(?:\.\d+)?)")


@dataclass(slots=True)
class Probe:
    width: int
    height: int
    duration: str
    r_frame_rate: str


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
            if not rx_fmt.match(path.name):
                raise argparse.ArgumentTypeError(f"invalid format '{path.name}'")
            if not path.parent.exists():
                if not OVERWITE:
                    if not rx_yes.match(input(MKDIR_MSG % path.parent.absolute())):
                        exit(0)
                path.parent.mkdir(parents=True, exist_ok=True)
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
        default=DEFAULT_COUNT,
        metavar="INT",
        help="frames count (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=check_format,
        default=DEFAULT_FMT,
        metavar="STR",
        help="output format (default: %(default)s), should include %%d format specifier",
    )
    parser.add_argument("-p", "--preview", action="store_true", help="generate preview")
    parser.add_argument(
        "-P",
        "--preview-output",
        metavar="STR",
        help="preview path (default: format based frames_output_dir/preview.png)",
    )
    parser.add_argument(
        "-t",
        "--preview-template",
        metavar="STR",
        help="preview tiling template (default: '{α}x{count/α}', where 'α' is square root of 'count')",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-y", action="store_true", help="confirm mkdir -p")

    return parser.parse_args()


def get_probe(file: str) -> Probe:
    try:
        match probe := json.loads(
            sp.check_output(PROBE_CMD % file, shell=True).decode()
        ):
            case {
                "streams": [
                    {
                        "width": int(),
                        "height": int(),
                        "duration": str(),
                        "r_frame_rate": str(),
                    }
                ]
            }:
                if streams := probe.get("streams", []):
                    return Probe(
                        **{
                            k: v
                            for k, v in streams[0].items()
                            if k in Probe.__annotations__
                        }
                    )
        raise Exception("unexpected probe format")
    except Exception as e:
        exit(str(e))


def get_interval(probe: Probe, framecount: int) -> float | None:
    try:
        if (duration := rx_dur.findall(probe.duration).pop()) and (
            fps := rx_fps.findall(probe.r_frame_rate).pop()
        ):
            return round((float(fps) * float(duration)) / framecount, 2)
        raise Exception("unexpected probe format")
    except Exception as e:
        print(e)


def generate_preview(args: argparse.Namespace, probe: Probe):
    def find_num(s: str) -> int:
        try:
            if match := rx_num.search(s):
                return int(match.group())
        except:
            pass
        return 0

    output = args.preview_output or Path(args.format.parent).joinpath(DEFAULT_PREVIEW)
    rows = args.count // int(math.sqrt(args.count))
    cols = args.count // rows
    # swap cols and rows for vertical aspect ratio
    if (probe.width / probe.height) < 1 and cols < rows:
        cols, rows = rows, cols

    template = args.preview_template or f"{cols}x{rows}"
    files = " ".join(
        f"{p}"
        for p in sorted(
            args.format.parent.glob(f"*{args.format.suffix}"),
            key=lambda f: find_num(f.stem),
        )[: cols * rows]
    )
    cmd = MOTAGE_CMD % (template, files, output)
    print(cmd)
    sp.run(cmd.split())


def check_executable(name) -> bool:
    code, _ = sp.getstatusoutput(f"which {name}")
    return code == 0


if __name__ == "__main__":
    if not check_executable(FFMPEG):
        exit(f"{FFMPEG} executable is not available")
    if not check_executable(FFPROBE):
        exit(f"{FFPROBE} executable is not available")

    args = parse_args()
    probe = get_probe(args.file)
    if interval := get_interval(probe, args.count):
        cmd = EXTRACT_CMD % (
            "" if args.verbose else SILENCE_OPTS,
            args.file,
            interval,
            args.count,
            args.format,
        )
        print(cmd)
        extract_process = sp.run(cmd.split())
        if extract_process.returncode == 0 and args.preview:
            if not check_executable(MONTAGE):
                exit(f"{MONTAGE} executable is not available")
            generate_preview(args, probe)
