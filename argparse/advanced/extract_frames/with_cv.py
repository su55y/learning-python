import argparse
import re
import os.path
from pathlib import Path

import cv2


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
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cap = cv2.VideoCapture(args.file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = num_frames / fps
    interval = int((fps * duration_sec) / args.count)
    frame_indices = [f for f in range(0, num_frames, interval)[:num_frames]]

    for i, frame in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret, frame = cap.read()
        if ret and i:
            cv2.imwrite(str(args.format) % i, frame)

    cap.release()
