import curses
from dataclasses import dataclass
from enum import IntEnum
import time
import threading
from typing import Sequence


class Key(IntEnum):
    j = ord("j")
    k = ord("k")
    g = ord("g")
    G = ord("G")
    q = ord("q")
    l = ord("l")
    h = ord("h")


@dataclass
class Line:
    text: str
    is_active: bool = False


class LinesPrinter:
    def __init__(self, lines: Sequence[str]) -> None:
        self.raw_lines = lines
        self.lines = list(map(Line, self.raw_lines))
        self.index = 0 if len(self.lines) else -1
        self.index_width = len(str(len(self.lines)))
        self.scroll_top = 0
        self.gravity = 0
        self._debug_info = ""

    def refresh_lines_active(self) -> None:
        for i in range(len(self.lines)):
            self.lines[i].is_active = i == self.index

    def update_scroll_top(self, max_rows: int) -> None:
        match self.gravity:
            case 0:
                if (self.index + 1) - self.scroll_top > max_rows:
                    self.scroll_top = (self.index + 1) - max_rows
                if self.index + 1 < self.scroll_top:
                    self.scroll_top = self.index
            case 1:
                if self.index + 1 == self.scroll_top:
                    self.scroll_top = max(self.scroll_top - 1, 0)
                if self.index + 1 == len(self.lines):
                    self.scroll_top = max((self.index + 1) - max_rows, 0)

    def run(self, stdscr: "curses._CursesWindow") -> None:
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_WHITE, 0)
        curses.init_pair(3, curses.COLOR_YELLOW, 0)
        max_y, max_x = stdscr.getmaxyx()
        status_window = curses.newwin(1, max_x, 0, 0)
        lines_window = curses.newwin(max_y, max_x - 1, 1, 0)

        def redraw_status(s: "curses._CursesWindow"):
            _, max_x = s.getmaxyx()
            time_str = time.strftime("%T")
            text = " %s, scroll_top: %d, index: %d%s " % (
                time_str,
                self.scroll_top,
                self.index,
                self._debug_info,
            )
            text = f"{text:^{max_x - 1}}"
            s.addnstr(0, 0, text, max_x - 2, curses.color_pair(1))
            s.refresh()

        def status_thread_loop(s: "curses._CursesWindow"):
            s.refresh()
            while True:
                redraw_status(s)
                time.sleep(1)

        status_thread = threading.Thread(
            target=status_thread_loop, daemon=True, args=(status_window,)
        )
        status_thread.start()

        while 1:
            stdscr.refresh()
            try:
                self.print_lines(lines_window)
            except Exception as e:
                input("Exception: %s" % e)
                exit(1)

            match stdscr.getch():
                case Key.q:
                    break
                case Key.j | curses.KEY_DOWN:
                    self.index = (self.index + 1) % len(self.lines)
                    self.gravity = 0
                case Key.k | curses.KEY_UP:
                    self.index = (self.index - 1) % len(self.lines)
                    self.gravity = 1
                case Key.l | curses.KEY_RIGHT:
                    self.switch_to_pad(lines_window)

    def print_status(self, status_window: "curses._CursesWindow") -> None:
        _, max_x = status_window.getmaxyx()
        status_window.addnstr(0, 1, "[%s]\n" % time.strftime("%T"), max_x - 2)

    def switch_to_pad(self, s: "curses._CursesWindow") -> None:
        s.clear()
        max_y, max_x = s.getmaxyx()
        pad_pos = self.scroll_top
        pad = curses.newpad(len(self.raw_lines) + 1, max_x)

        def redraw_pad(pad, max_x):
            for i, line in enumerate(self.raw_lines):
                text = f"{i:{self.index_width}d} {line}"
                pad.addnstr(i, 0, text, min(len(text), max_x))

        redraw_pad(pad, max_x)
        pad.refresh(pad_pos, 0, 1, 0, max_y - 1, max_x - 1)
        s.refresh()

        while True:
            max_y, max_x = s.getmaxyx()
            pad.refresh(pad_pos, 0, 1, 0, max_y - 1, max_x - 1)

            match s.getch():
                case Key.h | curses.KEY_LEFT | Key.q:
                    s.clear()
                    break
                case Key.j | curses.KEY_DOWN:
                    pad_pos = min(pad_pos + 1, pad.getyx()[0] - max_y)
                case Key.k | curses.KEY_UP:
                    pad_pos = max(0, pad_pos - 1)

    def print_lines(self, s: "curses._CursesWindow") -> None:
        max_y, max_x = s.getmaxyx()
        y, x = 0, 1
        max_rows = max_y - 1
        self.update_scroll_top(max_rows)
        self.refresh_lines_active()
        for i, line in enumerate(
            self.lines[self.scroll_top : self.scroll_top + max_rows]
        ):
            text = f"%s %{self.index_width}d) %s\n" % (
                ">" if line.is_active else " ",
                i + self.scroll_top,
                line.text,
            )
            width = min(max_x - 1, len(text))
            color_pair = curses.color_pair(2)
            if line.is_active:
                color_pair = curses.color_pair(3)

            try:
                s.addnstr(y, x, text, width, color_pair)
            except:
                pass
            # s.addnstr(y, x, text, width, color_pair)
            y += 1
        s.refresh()


def read_self_lines() -> list[str]:
    with open(__file__) as f:
        return f.readlines()


if __name__ == "__main__":
    lines = read_self_lines()
    try:
        curses.wrapper(LinesPrinter(lines).run)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
