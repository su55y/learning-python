#!/usr/bin/env -S python -u

from pathlib import Path
from subprocess import run
from typing import Final

ASCII_UPPER = (65, 91)
ASCII_LOWER = (97, 123)
UPPER_DIFF: Final[int] = 120107
LOWER_DIFF: Final[int] = 120101


def translate_text(s: str) -> str:
    res = ""
    for c in list(s):
        a = ord(c)
        if a >= ASCII_UPPER[0] and ASCII_UPPER[1] > a:
            res += chr(a + UPPER_DIFF)
        elif a >= ASCII_LOWER[0] and ASCII_LOWER[1] > a:
            res += chr(a + LOWER_DIFF)
        else:
            res += c
    return res.strip()


def to_clipboard(s: str):
    run(["xsel", "-b"], input=s.encode())


if __name__ == "__main__":
    theme_path = Path(__file__).resolve().parent.joinpath("theme.rasi")
    rofi_cmd = ("rofi -dmenu -no-config -theme %s" % theme_path).split()
    res = run(rofi_cmd, capture_output=True)
    if res.returncode == 0:
        to_clipboard(translate_text(res.stdout.decode()))
