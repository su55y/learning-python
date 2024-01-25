import curses
import time
from typing import Sequence


class LinesPrinter:
    def __init__(self, lines: Sequence[str]) -> None:
        self.lines = lines
        self.active_index = 0 if len(self.lines) else -1

    def run(self, stdscr: "curses._CursesWindow") -> None:
        curses.curs_set(0)
        self.s = stdscr
        while 1:
            try:
                self.print_lines()
            except:
                pass
            match chr(_ := self.s.getch()):
                case "q":
                    break
                case "j":
                    self.active_index = (self.active_index + 1) % len(self.lines)
                case "k":
                    self.active_index = (self.active_index - 1) % len(self.lines)

    def print_lines(self) -> None:
        self.s.clear()
        curses.update_lines_cols()
        self.s.addstr("[%s] %d lines\n" % (time.strftime("%T"), curses.LINES))
        for i, line in enumerate(self.lines[: curses.LINES - 1]):
            self.s.addstr("%s %s\n" % (">" if i == self.active_index else " ", line))


if __name__ == "__main__":
    curses.wrapper(LinesPrinter(tuple(chr(i) * 3 for i in range(97, 100))).run)
