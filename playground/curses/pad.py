import curses
from typing import List


def read_self_lines() -> List[str]:
    with open(__file__) as f:
        return f.readlines()


def main(scr: "curses._CursesWindow"):
    curses.use_default_colors()
    curses.curs_set(0)
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

        match chr(ch := scr.getch()):
            case "j":
                pad_pos = min(pad_pos + 1, pad.getyx()[0] - h)
            case "k":
                pad_pos = max(0, pad_pos - 1)
            case "g":
                pad_pos = 0
            case "G":
                pad_pos = pad.getyx()[0] - h
            case "q":
                break
            case _:
                if ch == curses.KEY_RESIZE:
                    pad = handle_resize(pad)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
