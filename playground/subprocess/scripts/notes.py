from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess as sp
import time


EDITOR = None
DEFAULT_NOTES_DIR_PATH = Path().home() / ".notes"
FILE_FMT = """
=============================
{date}
=============================


""".format(
    date=time.strftime("%A, %d %B %Y")
)


@dataclass
class Config:
    notes_dir: Path


def default_config() -> Config:
    return Config(notes_dir=DEFAULT_NOTES_DIR_PATH)


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

        if not self.today_file.exists():
            with open(self.today_file, "w") as f:
                f.write(FILE_FMT)


def get_last_line(filepath: Path) -> str:
    return sp.getoutput(f"tail -n 1 {filepath!s}").strip()


if __name__ == "__main__":
    config = default_config()
    EDITOR = os.environ.get("EDITOR", None)
    if EDITOR is None:
        print("EDITOR env is not set")
        exit(1)

    notes = Notes(config)

    p = sp.run([EDITOR, str(notes.today_file), "+"], capture_output=False)
    if p.returncode != 0:
        exit(1)

    last_line = get_last_line(notes.today_file)
    if last_line != "":
        with open(notes.today_file, "a") as f:
            f.write("\n\n")
