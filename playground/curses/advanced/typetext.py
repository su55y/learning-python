import argparse
import curses
from curses.textpad import rectangle as curses_rect
from enum import IntEnum
from functools import lru_cache
import random
import re
from pathlib import Path
import string
import threading
import time

valid_keys = set(map(ord, string.ascii_lowercase))
valid_chars = {" ", *string.ascii_lowercase}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--words-count",
        type=int,
        default=10,
        metavar="INT",
        help="Words count (default: %(default)s)",
    )
    return parser.parse_args()


def rnd_words(words: list[str], words_count: int = 10) -> list[str]:
    return random.choices(words, k=words_count)


def read_self_words() -> list[str]:
    reader = (row for row in open(Path(__file__)))
    rx = re.compile(r"[^a-zA-Z\s]")
    words_ = set()
    for row in reader:
        row_words = rx.sub(" ", row).split()
        if len(row_words) > 0:
            words_ |= set(row_words)
    return list(map(lambda w: w.lower(), filter(lambda w: len(w) > 1, words_)))


class Key(IntEnum):
    BACKSPACE = 263
    CTRL_R = 18
    r = ord("r")
    q = ord("q")


@lru_cache(len(valid_chars))
def validate_char(char: str) -> bool:
    return char in valid_chars


class CharState(IntEnum):
    Default = 0
    Correct = 1
    Wrong = 2


class Char:
    def __init__(self, char: str) -> None:
        assert len(char) == 1
        assert validate_char(char[0]) is True
        self.char = char[0]
        self.input = ""

    @property
    def state(self) -> CharState:
        if not self.input:
            return CharState.Default
        if self.char == self.input:
            return CharState.Correct
        if self.char == " ":
            return CharState.Default
        return CharState.Wrong

    def __str__(self) -> str:
        return self.char[0]


class CursorPos:
    def __init__(self, length: int) -> None:
        self.min = 0
        self.max = max(0, length)
        self._current = 0

    def increment(self) -> None:
        if not self.is_increment_valid:
            return
        self._current += 1

    def decrement(self) -> None:
        if not self.is_decrement_valid:
            return
        self._current -= 1

    @property
    def current(self) -> int:
        return self._current

    @current.setter
    def current(self, value: int) -> None:
        self._current = value

    @property
    def is_increment_valid(self) -> bool:
        return self._current + 1 <= self.max

    @property
    def is_decrement_valid(self) -> bool:
        return self._current - 1 >= self.min


class Chars:
    def __init__(self, game_words: list[str]) -> None:
        assert len(game_words) > 0
        self.words = game_words
        self.chars = self.build_chars(self.words)
        self.chars_count = sum(map(len, game_words))
        self.pos = CursorPos(length=sum(map(len, game_words)))
        self._correct_chars = 0
        self._wrong_chars = 0

    def update_char(self, char: str) -> bool:
        pos = 0
        for i in range(len(self.chars)):
            for j in range(len(self.chars[i])):
                if pos == self.pos.current:
                    self.chars[i][j].input = char
                    return True
                pos += 1
        return False

    def move_forward(self, char: str) -> None:
        if self.update_char(char):
            self.pos.increment()

    def move_backwards(self) -> None:
        if not self.pos.is_decrement_valid:
            return
        if self.pos.current > 0:
            self.pos.decrement()
        if not self.update_char(""):
            self.pos.increment()

    @property
    def correct_chars(self) -> int:
        correct = 0
        for w in self.chars:
            correct += len(list(filter(lambda c: c.state == CharState.Correct, w)))
        return correct

    @property
    def wrong_chars(self) -> int:
        wrong = 0
        for w in self.chars:
            wrong += len(list(filter(lambda c: c.state == CharState.Wrong, w)))
        return wrong

    @property
    def correct_words(self) -> int:
        c = 0
        for word in self.chars:
            if all(ch.input == ch.char for ch in word):
                c += 1
        return c

    @staticmethod
    def build_chars(words_: list[str]) -> list[list[Char]]:
        chars: list[list[Char]] = list()
        for word in words_:
            chars.append(list(map(Char, word)))
        return chars


class Game:
    def __init__(self, words: list[str], words_count: int) -> None:
        self.src_words = words
        self.words_count = words_count

        self.words = rnd_words(self.src_words, self.words_count)
        self.chars = Chars(self.words)
        self.start_perf_time = -1

        self.fg_yellow = 0
        self.fg_red = 0
        self.bg_white = 0
        self.status_color = 0

        self.default_status_fmt = " start typing..."
        self.status_fmt = self.default_status_fmt
        self.chars_stats_fmt = " correct: {correct} | wrong: {wrong} | left: {left}"

    def reset(self, stdscr: "curses._CursesWindow") -> None:
        stdscr.clear()
        self.words = rnd_words(self.src_words, self.words_count)
        self.chars = Chars(self.words)
        self.start_perf_time = -1
        self.status_fmt = self.default_status_fmt
        self.run(stdscr)

    def run(self, stdscr: "curses._CursesWindow") -> None:
        self._setup_curses()
        self._run_loop(stdscr)

    def _setup_curses(self) -> None:
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_YELLOW, 0)
        curses.init_pair(2, curses.COLOR_RED, 0)
        curses.init_pair(3, 0, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        self.fg_yellow = curses.color_pair(1)
        self.fg_red = curses.color_pair(2)
        self.bg_white = curses.color_pair(3)
        self.status_color = curses.color_pair(4)

    def _run_loop(self, stdscr: "curses._CursesWindow") -> None:
        max_y, max_x = stdscr.getmaxyx()
        game_win = curses.newwin(max_y - 2, max_x, 0, 0)
        status_win = curses.newwin(1, max_x, max_y - 1, 0)
        stdscr.refresh()
        status_thread = threading.Thread(
            target=self._run_status_loop, daemon=True, args=(status_win,)
        )
        status_thread.start()
        while True:
            self.print_words_by_rows(game_win)
            self.print_status(status_win)
            ch = stdscr.getch()
            if ch == Key.CTRL_R:
                self.reset(stdscr)
                return
            if ch == Key.BACKSPACE:
                self.chars.move_backwards()
            elif ch in valid_keys:
                if self.start_perf_time < 0:
                    self.start_perf_time = time.perf_counter()
                    self.status_fmt = self.chars_stats_fmt
                    self.print_status(status_win)

                self.chars.move_forward(chr(ch))

                if self.chars.pos.max == self.chars.pos.current:
                    self.chars.pos.current += 1
                    self.print_words_by_rows(game_win)
                    self.chars.pos.current -= 1
                    self._run_winscreen_loop(stdscr, status_win)
                    return

            stdscr.refresh()

    def print_words_by_rows(self, game_win: "curses._CursesWindow") -> None:
        start_y, start_x = 2, 2
        y, x = start_y, start_x
        max_y, max_x = game_win.getmaxyx()
        pos = 0
        row_len = 0
        for word in self.chars.chars:
            if (row_len + len(word) + 3) >= max_x:
                y += 1
                x = start_x
                row_len = 0
            row_len += len(word) + 1
            if y >= max_y - 1:
                break
            for char in word:
                self.print_char(game_win, y, x, char, pos)
                pos += 1
                x += 1
            game_win.addnstr(y, x, " ", 1, 0)
            x += 1

        if y + 2 < max_y:
            curses_rect(game_win, 0, 0, y + 2, max_x - 1)
        game_win.refresh()

    def print_char(
        self,
        game_win: "curses._CursesWindow",
        y: int,
        x: int,
        char: Char,
        pos: int,
    ) -> None:
        color_pair = 0
        if char.state == CharState.Correct:
            color_pair = self.fg_yellow
        elif char.state == CharState.Wrong:
            color_pair = self.fg_red
        if self.chars.pos.current == pos:
            color_pair = self.bg_white
        game_win.addnstr(y, x, char.char, 1, color_pair)

    def _run_winscreen_loop(
        self,
        stdscr: "curses._CursesWindow",
        status_win: "curses._CursesWindow",
    ) -> None:
        elapsed = time.perf_counter() - self.start_perf_time
        self.start_perf_time = -1
        wpm = 60 / elapsed * self.chars.correct_words
        acc = (self.chars.correct_chars / self.chars.chars_count) * 100
        stats = f"time: {elapsed:.1f}s | wpm: {wpm:.2f} | acc: {acc:.2f}%"
        self.status_fmt = f"{self.status_fmt} | {stats} | [r]: restart | [q]: quit"
        self.print_status(status_win)
        while True:
            match stdscr.getch():
                case Key.r:
                    self.reset(stdscr)
                    return
                case Key.q:
                    break

    def _run_status_loop(self, status_win: "curses._CursesWindow") -> None:
        while True:
            self.print_status(status_win)
            time.sleep(1)

    def print_status(self, status_win: "curses._CursesWindow") -> None:
        _, max_x = status_win.getmaxyx()
        status_str = self.format_status()
        status_win.addnstr(0, 0, f"{status_str:<{max_x - 1}}", max_x, self.status_color)
        status_win.refresh()

    def format_status(self) -> str:
        return self.status_fmt.format(
            correct=self.chars.correct_chars,
            wrong=self.chars.wrong_chars,
            left=self.chars.chars_count - self.chars.pos.current,
        )


def main():
    args = parse_args()
    game = Game(read_self_words(), args.words_count)
    try:
        curses.wrapper(game.run)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
