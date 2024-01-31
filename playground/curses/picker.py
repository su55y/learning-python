import curses
from dataclasses import dataclass
from enum import IntEnum
import random
from typing import Sequence


@dataclass
class Line:
    text: str
    is_active: bool = False


class Key(IntEnum):
    j = ord("j")
    k = ord("k")
    g = ord("g")
    G = ord("G")
    q = ord("q")
    ESC = 27
    RETURN = ord("\n")


class Picker:
    def __init__(self, lines: Sequence[str]) -> None:
        self.lines = list(map(Line, lines))
        self.index = 0
        self.gravity = 1
        self.last_scroll_pos = 0

    def move_up(self) -> None:
        self.gravity = 0
        self.index -= 1
        if self.index < 0:
            self.index = len(self.lines) - 1

    def move_down(self) -> None:
        self.gravity = 1
        self.index += 1
        if self.index >= len(self.lines):
            self.index = 0

    def refresh_lines(self) -> None:
        for i in range(len(self.lines)):
            self.lines[i].is_active = i == self.index

    def draw(self, screen: "curses._CursesWindow") -> None:
        screen.clear()
        x, y = 1, 0
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y - 1

        self.refresh_lines()
        current_line = self.index + 1
        scroll_top = self.last_scroll_pos

        if self.gravity == 1:
            if current_line > max_rows:
                scroll_top += 1
            if current_line == len(self.lines):
                scroll_top = max(current_line - max_rows, 0)
            if current_line == 1:
                scroll_top = 0
        else:
            if current_line == scroll_top:
                scroll_top = max(scroll_top - 1, 0)
            if current_line == len(self.lines):
                scroll_top = max(current_line - max_rows, 0)

        self.last_scroll_pos = scroll_top

        for line in self.lines[scroll_top : scroll_top + max_rows]:
            if line.is_active:
                screen.attron(curses.color_pair(1))
                screen.addnstr(y, x, line.text, max_x - 2)
                screen.attroff(curses.color_pair(1))
            else:
                screen.addnstr(y, x, line.text, max_x - 2)
            y += 1

        screen.attron(curses.color_pair(2))
        status = " current: %d, scroll_top: %d, max_rows: %d, gravity: %s" % (
            current_line,
            scroll_top,
            max_rows,
            "Down" if self.gravity else "Up",
        )
        screen.addnstr(max_y - 1, x, f"{status:<{max_x-2}}", max_x - 2)
        screen.attroff(curses.color_pair(2))

        screen.refresh()

    def run_loop(self, screen: "curses._CursesWindow") -> int:
        while True:
            self.draw(screen)
            match screen.getch():
                case Key.j | curses.KEY_DOWN:
                    self.move_down()
                case Key.k | curses.KEY_UP:
                    self.move_up()
                case Key.q | Key.ESC:
                    exit(0)
                case Key.RETURN | curses.KEY_ENTER:
                    return self.index

    def config_curses(self) -> None:
        try:
            curses.use_default_colors()
            curses.curs_set(0)
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        except:
            curses.initscr()

    def _start(self, screen: "curses._CursesWindow"):
        self.config_curses()
        return self.run_loop(screen)

    def start(self):
        return curses.wrapper(self._start)


if __name__ == "__main__":
    lines = [
        f"{x-96} " + (f"{chr(x)}" * random.randint(30, 80)) for x in range(97, 108)
    ]
    # lines += [" "] + lines
    choice = Picker(lines).start()
    print(f"Your choice: {lines[choice]!r}")
