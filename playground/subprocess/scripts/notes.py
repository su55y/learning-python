from pathlib import Path
import re
import subprocess as sp
import time


NOTES_DIR_PATH = Path().home() / ".notes"
MONTH_DIR = NOTES_DIR_PATH / time.strftime("%Y_%02m")
TODAY_FILE = MONTH_DIR / time.strftime("%d")
FILE_FMT = """
=============================
{date}
=============================


""".format(
    date=time.strftime("%A, %d %B %Y")
)


def init():
    if not NOTES_DIR_PATH.exists():
        resp = input(f"Directory {NOTES_DIR_PATH} not exists, create it? [y/n]: ")
        if not re.match("[yY](?:es)?", resp, flags=re.IGNORECASE):
            exit(0)

        NOTES_DIR_PATH.mkdir(mode=0o755)
    if not MONTH_DIR.exists():
        MONTH_DIR.mkdir(mode=0o755)

    if not TODAY_FILE.exists():
        with open(TODAY_FILE, "w") as f:
            f.write(FILE_FMT)


def last_line(filepath: Path) -> str:
    return sp.getoutput(f"tail -n 1 {filepath!s}").strip()


if __name__ == "__main__":
    init()
    p = sp.run(["nvim", str(TODAY_FILE), "+"], capture_output=False)
    if p.returncode != 0:
        exit(1)

    line = last_line(TODAY_FILE)
    if line != "":
        with open(TODAY_FILE, "a") as f:
            f.write("\n\n")
