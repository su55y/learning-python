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
    for i, line in enumerate(pad_content):
        pad.addstr("%d %s" % (i + 1, line))

    while 1:
        h, w = scr.getmaxyx()
        pad.refresh(pad_pos, 0, 0, 0, h - 1, w)

        match chr(ch := scr.getch()):
            case "j":
                if pad_pos < pad.getyx()[0] - h:
                    pad_pos += 1
            case "k":
                if pad_pos > 0:
                    pad_pos -= 1
            case "g":
                pad_pos = 0
            case "G":
                pad_pos = len(pad_content) - h
            case "q":
                break
            case _:
                if ch == curses.KEY_RESIZE:
                    h, *_ = scr.getmaxyx()
                    while pad_pos > pad.getyx()[0] - h:
                        pad_pos -= 1


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
