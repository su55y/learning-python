import curses
from dataclasses import dataclass
from enum import Enum, IntEnum
import os
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
    class Gravity(Enum):
        DOWN = 0
        UP = 1

        def __str__(self) -> str:
            return str(self.name)

    def __init__(self, lines: Sequence[str]) -> None:
        self.lines = list(map(Line, lines))
        self.index = 0
        self.gravity = self.Gravity.DOWN
        self.scroll_top = 0

    def move_up(self) -> None:
        self.gravity = self.Gravity.UP
        self.index = (self.index - 1) % len(self.lines)

    def move_down(self) -> None:
        self.gravity = self.Gravity.DOWN
        self.index = (self.index + 1) % len(self.lines)

    def refresh_lines(self) -> None:
        for i in range(len(self.lines)):
            self.lines[i].is_active = i == self.index

    def update_scroll_top(self, max_rows: int) -> None:
        match self.gravity:
            case self.Gravity.DOWN:
                if (self.index + 1) - self.scroll_top > max_rows:
                    self.scroll_top = (self.index + 1) - max_rows
                if self.index + 1 < self.scroll_top:
                    self.scroll_top = self.index
            case self.Gravity.UP:
                if self.index + 1 == self.scroll_top:
                    self.scroll_top = max(self.scroll_top - 1, 0)
                if self.index + 1 == len(self.lines):
                    self.scroll_top = max((self.index + 1) - max_rows, 0)

    @property
    def status(self) -> str:
        return " index: %d, scroll_top: %d, gravity: %s" % (
            self.index,
            self.scroll_top,
            self.gravity,
        )

    def draw(self, screen: "curses._CursesWindow") -> None:
        screen.clear()
        x, y = 1, 0
        max_y, max_x = screen.getmaxyx()
        max_rows = max_y - y - 1
        self.update_scroll_top(max_rows)
        self.refresh_lines()

        for line in self.lines[self.scroll_top : self.scroll_top + max_rows]:
            if line.is_active:
                screen.attron(curses.color_pair(1))
                screen.addnstr(y, x, line.text, max_x - 2)
                screen.attroff(curses.color_pair(1))
            else:
                screen.addnstr(y, x, line.text, max_x - 2)
            y += 1

        screen.attron(curses.color_pair(2))
        screen.addnstr(max_y - 1, x, f"{self.status:<{max_x-2}}", max_x - 2)
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
    w, _ = os.get_terminal_size()
    lines = [
        "%d %s" % (x - 96, f"{chr(x)}" * random.randint(1, w - 1))
        for x in range(97, 123)
    ]
    choice = Picker(lines).start()
    print(f"Your choice: {lines[choice]!r}")
