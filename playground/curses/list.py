import curses
import time
from typing import Sequence


class LinesPrinter:
    def __init__(self, lines: Sequence[str]) -> None:
        self.lines = lines

    def run(self, stdscr: "curses._CursesWindow") -> None:
        curses.curs_set(0)
        self.s = stdscr
        while 1:
            self.print_lines()
            match chr(_ := self.s.getch()):
                case "q":
                    break

    def print_lines(self) -> None:
        self.s.clear()
        self.s.addstr("[%s] %d lines\n" % (time.strftime("%T"), curses.LINES))
        for line in self.lines[: curses.LINES - 1]:
            self.s.addstr("%s\n" % line)
        self.s.refresh()


if __name__ == "__main__":
    curses.wrapper(LinesPrinter(("aaa", "bbb", "ccc")).run)
