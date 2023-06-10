#!/usr/bin/env python

from enum import Enum
import os
import sys
import subprocess as sp
from typing import Final


ROFI_RETV: Final[str] = os.getenv("ROFI_RETV", "")
ROFI_INFO: Final[str] = os.getenv("ROFI_INFO", "")

LINES = ("line #{n}\000info\037info #{n}".format(n=n) for n in range(5))
OPTIONS = (
    "\000message\037Press Ctrl+s to show secret entry",
    "\000use-hot-keys\037true",
    "\000markup-rows\037true",
)


class State(Enum):
    NULL = ""
    INITIAL = "0"
    SELECTED = "1"
    SELECTED_CUSTOM = "2"
    KB_CUSTOM_1 = "10"
    KB_CUSTOM_2 = "11"

    @staticmethod
    def get_state() -> "State":
        return State(ROFI_RETV)


if __name__ == "__main__":
    for opt in OPTIONS:
        print(opt)
    input = " ".join(sys.argv[1:])
    msg = lambda text: print("\000message\037%s" % text)

    match State.get_state():
        case State.INITIAL:
            pass
        case State.SELECTED:
            if ROFI_INFO == "secret":
                secret_cmd = "mpv https://youtu.be/dQw4w9WgXcQ".split()
                sp.Popen(secret_cmd, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                sys.exit(0)
            else:
                msg(f"you choosed '{input}', with info: '{ROFI_INFO}'")
        case State.SELECTED_CUSTOM:
            msg("you typed: %s" % input)
        case State.KB_CUSTOM_1:
            msg("secret line revealed")
            print("secret\000info\037secret")
            print("\000new-selection\0370")
        case _:
            sys.exit(1)
    for line in LINES:
        print(line)
