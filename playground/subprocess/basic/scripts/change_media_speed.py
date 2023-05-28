import argparse
from enum import Enum, auto
import json
import subprocess as sp
from sys import argv
from typing import Optional

FFMPEG_CMD = "ffmpeg %s -i %s %s %s"
SILENCE_OPTS = "-hide_banner -loglevel warning -stats"
PROBE_CMD = "ffprobe -v quiet -show_streams -of json %s"

SET_PTS = "setpts=PTS/%.3f"
ATEMPO = "atempo=%.3f"
FILTER_V = "-filter:v %s"
FILTER_A = "-filter:a %s"
COMPLEX_FILTER = "-filter_complex [0:v]%s[v];[0:a]%s[a] -map [v] -map [a]"


class MediaType(Enum):
    VideoOnly = auto()
    AudioOnly = auto()
    VideoAudio = auto()


# TODO: adjust aratio to more then 2.0 by concating


def get_filter(file: str, ratio: float) -> Optional[str]:
    probe = json.loads(sp.getoutput(PROBE_CMD % file))
    match probe:
        case {"streams": list()}:
            # TODO: bruh
            filter_type = None
            for stream in probe.get("streams"):
                match stream.get("codec_type"):
                    case "video":
                        filter_type = (
                            MediaType.VideoAudio
                            if filter_type == MediaType.AudioOnly
                            else MediaType.VideoOnly
                        )
                    case "audio":
                        filter_type = (
                            MediaType.VideoAudio
                            if filter_type == MediaType.VideoOnly
                            else MediaType.AudioOnly
                        )

            if not filter_type:
                raise Exception("can't find video or audio stream")

            match filter_type:
                case MediaType.VideoOnly:
                    return FILTER_V % (SET_PTS % ratio)
                case MediaType.AudioOnly:
                    return FILTER_A % (ATEMPO % ratio)
                case MediaType.VideoAudio:
                    return COMPLEX_FILTER % (SET_PTS % ratio, ATEMPO % ratio)

            raise Exception("can't choose filter")


def parse_args() -> Optional[argparse.Namespace]:
    def validate_ratio(v) -> float:
        try:
            if (r := float(v)) and (r < 0.5 or r > 2.0):
                raise argparse.ArgumentTypeError("ratio should be in range 0.5 - 2.0")
        except Exception as e:
            exit(repr(e))
        else:
            return r

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    parser.add_argument("-o", "--output", required=True, help="output file")
    parser.add_argument(
        "-r",
        "--ratio",
        type=validate_ratio,
        required=True,
        help="speed ratio (should be in range 0.5 - 2.0)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args() or exit("can't parse args")

    try:
        filter = get_filter(args.input, args.ratio)
    except Exception as e:
        exit(repr(e))

    cmd = FFMPEG_CMD % (
        "" if args.verbose else SILENCE_OPTS,
        argv[1],
        filter,
        args.output,
    )
    if args.verbose:
        print(f"run '{cmd}'\n")
    sp.run(cmd.split())