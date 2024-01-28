from enum import IntEnum
import curses
from typing import List


class Key(IntEnum):
    j = ord("j")
    k = ord("k")
    g = ord("g")
    G = ord("G")
    q = ord("q")


def read_self_lines() -> List[str]:
    with open(__file__) as f:
        return f.readlines()


def main(scr: "curses._CursesWindow"):
    curses.use_default_colors()
    curses.curs_set(0)
    scr.keypad(True)
    curses.mousemask(-1)
    scr.refresh()

    pad_height = (2 << 14) - 1
    pad = curses.newpad(pad_height, scr.getmaxyx()[-1])
    pad_pos = 0

    pad_content = read_self_lines()

    def add_lines(pad):
        for i, line in enumerate(pad_content):
            pad.addstr("%d %s" % (i + 1, line))

    def handle_resize(pad):
        pad.clear()
        h, w = scr.getmaxyx()
        pad = curses.newpad(pad_height, w)
        add_lines(pad)
        pad.refresh(pad_pos, 0, 0, 0, h - 1, w - 1)
        scr.refresh()
        return pad

    add_lines(pad)
    while 1:
        h, w = scr.getmaxyx()
        pad.refresh(pad_pos, 0, 0, 0, h - 1, w - 1)

        match scr.getch():
            case Key.j | curses.KEY_DOWN:
                pad_pos = min(pad_pos + 1, pad.getyx()[0] - h)
            case Key.k | curses.KEY_UP:
                pad_pos = max(0, pad_pos - 1)
            case Key.g | curses.KEY_LEFT:
                pad_pos = 0
            case Key.G | curses.KEY_RIGHT:
                pad_pos = pad.getyx()[0] - h
            case Key.q:
                break
            case curses.KEY_RESIZE:
                pad = handle_resize(pad)
            case curses.KEY_MOUSE:
                match curses.getmouse()[-1]:
                    case curses.BUTTON4_PRESSED:
                        pad_pos = max(0, pad_pos - 1)
                    case curses.BUTTON5_PRESSED:
                        pad_pos = min(pad_pos + 1, pad.getyx()[0] - h)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
