import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess as sp
import time
import toml


DEFAULT_NOTES_DIR_PATH = Path().home() / ".notes"
FILE_FMT = """
=============================
{date}
=============================


""".format(
    date=time.strftime("%A, %d %B %Y")
)


def str2path(v: str) -> Path:
    return Path(v).expanduser()


@dataclass
class Config:
    notes_dir: Path
    editor: str = ""

    def __post_init__(self):
        if isinstance(self.notes_dir, str):
            self.notes_dir = str2path(self.notes_dir)
        if len(self.editor) == 0:
            EDITOR = os.environ.get("EDITOR", None)
            if EDITOR is None:
                print("EDITOR env is not set")
                exit(1)
            self.editor = EDITOR


def default_config() -> Config:
    return Config(notes_dir=DEFAULT_NOTES_DIR_PATH)


def default_config_path() -> Path:
    config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    return Path(config_home) / "notes/config.toml"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        default=default_config_path(),
        type=str2path,
        metavar="PATH",
        help="config file path (default: %(default)s)",
    )
    parser.add_argument(
        "-i",
        "--inspect",
        action="store_true",
        help="inspect notes files",
    )
    parser.add_argument(
        "-I",
        "--inspect-loop",
        action="store_true",
        help="inspect notes files in loop",
    )
    return parser.parse_args()


class Notes:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.notes_dir = self.config.notes_dir
        self.month_dir = self.notes_dir / time.strftime("%Y_%02m")
        self.today_file = self.month_dir / time.strftime("%02d")
        self._init_files()

    def _init_files(self):
        if not self.notes_dir.exists():
            resp = input(f"Directory {self.notes_dir} not exists, create it? [y/n]: ")
            if not re.match("[yY](?:es)?", resp, flags=re.IGNORECASE):
                exit(0)

            self.notes_dir.mkdir(mode=0o755)
        if not self.month_dir.exists():
            self.month_dir.mkdir(mode=0o755)

    def edit(self):
        is_new = False
        if not self.today_file.exists():
            with open(self.today_file, "w") as f:
                f.write(FILE_FMT)
                is_new = True

        p = sp.run(
            [self.config.editor, str(self.today_file), "+"],
            capture_output=False,
        )
        if p.returncode != 0:
            exit(1)

        if is_new and len(FILE_FMT) == self.today_file.stat().st_size:
            self.today_file.unlink()
            return

        last_line = get_last_line(self.today_file)
        if last_line != "":
            with open(self.today_file, "a") as f:
                f.write("\n\n")


def get_last_line(filepath: Path) -> str:
    return sp.getoutput(f"tail -n 1 {filepath!s}").strip()


def choose_file(dir: Path) -> Path:
    nth_len = len(str(dir).split("/"))
    code, out = sp.getstatusoutput(
        f"""find {dir!s} -type f |\
                sort -r |\
                fzf -d/ --with-nth {nth_len}..\
                --bind='ctrl-d:execute-silent(rm {{}})+reload(\
                find {dir!s} -type f | sort -r)+clear-query'"""
    )
    if code != 0:
        exit(1)
    return Path(out)


if __name__ == "__main__":
    args = parse_args()
    if args.config.exists():
        with open(args.config) as f:
            config = Config(**toml.load(f))
    else:
        config = default_config()

    notes = Notes(config)

    def inspect():
        file = choose_file(config.notes_dir)

        p = sp.run(
            [config.editor, str(file), "+"],
            capture_output=False,
        )
        if p.returncode != 0:
            exit(1)

    if args.inspect:
        inspect()
    elif args.inspect_loop:
        while 1:
            inspect()
    else:
        notes.edit()
