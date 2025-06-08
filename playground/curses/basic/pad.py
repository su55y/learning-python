from enum import IntEnum
import curses
from typing import List


class Key(IntEnum):
    j = ord("j")
    k = ord("k")
    g = ord("g")
    G = ord("G")
    q = ord("q")
    l = ord("l")
    h = ord("h")


def read_self_lines() -> List[str]:
    with open(__file__) as f:
        return f.readlines()


def main(scr: curses.window):
    curses.use_default_colors()
    curses.curs_set(0)
    scr.keypad(True)
    curses.mousemask(-1)
    scr.refresh()

    self_lines = read_self_lines()
    rev_self_lines = list(map(lambda s: s[::-1].strip(), self_lines))
    pad_content = self_lines
    state = 0
    pad_pos = 0
    pad_height = len(pad_content) + 1
    pad = curses.newpad(pad_height, scr.getmaxyx()[-1])

    def redraw_pad(pad):
        _, w = scr.getmaxyx()
        for i, line in enumerate(pad_content):
            if state == 1:
                text = "%s %2d" % (line, i + 1)
                text = f"{text:>{w}}"
            else:
                text = "%2d %s" % (i + 1, line)
                text = f"{text:<{w}}"
            pad.addnstr(i, 0, text, min(len(text), w))

    def handle_resize(pad):
        pad.clear()
        h, w = scr.getmaxyx()
        pad = curses.newpad(pad_height, w)
        redraw_pad(pad)
        pad.refresh(pad_pos, 0, 0, 0, h - 1, w - 1)
        scr.refresh()
        return pad

    redraw_pad(pad)
    while 1:
        h, w = scr.getmaxyx()
        pad.refresh(pad_pos, 0, 0, 0, h - 1, w - 1)

        match scr.getch():
            case Key.j | curses.KEY_DOWN:
                pad_pos = min(pad_pos + 1, pad.getyx()[0] - h)
            case Key.k | curses.KEY_UP:
                pad_pos = max(0, pad_pos - 1)
            case Key.g:
                pad_pos = 0
            case Key.G:
                pad_pos = pad.getyx()[0] - h
            case Key.l | curses.KEY_RIGHT:
                if state == 0:
                    pad_content = rev_self_lines
                    state = 1
                    redraw_pad(pad)
            case Key.h | curses.KEY_LEFT:
                if state == 1:
                    pad_content = self_lines
                    state = 0
                    redraw_pad(pad)
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
