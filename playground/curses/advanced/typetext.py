import argparse
import curses
from curses.textpad import rectangle as curses_rect
from enum import IntEnum, Enum, auto as enum_auto
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
    parser.add_argument(
        "-f", "--words-file", type=Path, help="Words file path in word per line format"
    )
    return parser.parse_args()


def read_self_words() -> list[str]:
    reader = (row for row in open(Path(__file__)))
    rx = re.compile(r"[^a-zA-Z\s]")
    words_ = set()
    for row in reader:
        row_words = rx.sub(" ", row).split()
        if len(row_words) > 0:
            words_ |= set(row_words)
    return list(map(lambda w: w.lower(), filter(lambda w: len(w) > 1, words_)))


def read_words_file(path: Path) -> list[str]:
    reader = (row for row in open(path))
    rx = re.compile(r"^[a-zA-Z]+$")
    words_ = set()
    for row in reader:
        row = row.strip()
        if rx.match(row):
            words_.add(row)
    return list(words_)


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
        self.avg_word_len = self.chars_count / len(game_words)
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

    @property
    def correct_chars_avg(self) -> float:
        return self.correct_chars / self.avg_word_len

    @property
    def penalty(self) -> float:
        return self.wrong_chars * max(0, self.wrong_chars / self.avg_word_len)

    @staticmethod
    def build_chars(words_: list[str]) -> list[list[Char]]:
        chars: list[list[Char]] = list()
        for word in words_:
            chars.append(list(map(Char, word)))
        return chars


class GameState(Enum):
    INIT = enum_auto()
    TYPING = enum_auto()
    WINSCREEN = enum_auto()


class Game:
    def __init__(self, words: list[str], words_count: int) -> None:
        self.src_words = words
        self.words_count = words_count

        self.words = self.rnd_words()
        self.chars = Chars(self.words)
        self.start_perf_time = -1
        self.status_thread_started = False
        self.state = GameState.INIT

        self.fg_yellow = 0
        self.fg_red = 0
        self.bg_white = 0
        self.status_color = 0

        self.default_status_fmt = " start typing..."
        self.status_fmt_ = self.default_status_fmt
        self.chars_stats_fmt = " correct: {correct} | wrong: {wrong} | left: {left}"
        self.winscreen_status_fmt = " time: {time:.1f}s | wpm: {wpm:.2f} | wpm (avg): {avg_wpm:.2f} | acc: {acc:.1f}% | [r]: restart | [q]: quit"
        self.time = 0
        self.wpm = 0
        self.avg_wpm = 0
        self.acc = 0

    def rnd_words(self) -> list[str]:
        return random.choices(self.src_words, k=self.words_count)

    def reset(self) -> None:
        self.words = self.rnd_words()
        self.chars = Chars(self.words)
        self.start_perf_time = -1
        self.state = GameState.INIT
        self.time = 0
        self.wpm = 0
        self.avg_wpm = 0
        self.acc = 0

    def run(self, stdscr: "curses._CursesWindow") -> None:
        self._setup_curses()
        self.stdscr = stdscr
        while self._run_loop():
            self.stdscr.clear()
            self.reset()

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

    @staticmethod
    def try_addnstr(stdscr: "curses._CursesWindow", *args) -> None:
        try:
            stdscr.addnstr(*args)
        except:
            pass

    def _run_loop(self) -> bool:
        max_y, max_x = self.stdscr.getmaxyx()
        self.game_win = curses.newwin(max_y - 2, max_x, 0, 0)
        self.status_win = curses.newwin(1, max_x, max_y - 1, 0)
        self.stdscr.refresh()
        if not self.status_thread_started:
            threading.Thread(
                target=self._run_status_loop,
                daemon=True,
            ).start()
        while True:
            self.print_words_by_rows()
            self.print_status()
            ch = self.stdscr.getch()
            if ch == Key.CTRL_R:
                return True
            if ch == Key.BACKSPACE:
                self.chars.move_backwards()
            elif ch in valid_keys:
                if self.state is GameState.INIT and self.start_perf_time < 0:
                    self.start_perf_time = time.perf_counter()
                    self.state = GameState.TYPING
                    self.print_status()

                self.chars.move_forward(chr(ch))

                if self.chars.pos.max == self.chars.pos.current:
                    self.chars.pos.current += 1
                    self.print_words_by_rows()
                    self.chars.pos.current -= 1
                    return self._run_winscreen_loop()

                self.stdscr.refresh()

    def print_words_by_rows(self) -> None:
        start_y, start_x = 2, 2
        y, x = start_y, start_x
        max_y, max_x = self.game_win.getmaxyx()
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
                self.print_char(y, x, char, pos)
                pos += 1
                x += 1
            self.try_addnstr(self.game_win, y, x, " ", 1, 0)
            x += 1

        if y + 2 < max_y:
            curses_rect(self.game_win, 0, 0, y + 2, max_x - 1)
        self.game_win.refresh()

    def print_char(
        self,
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
        self.try_addnstr(self.game_win, y, x, char.char, 1, color_pair)

    def _run_winscreen_loop(self) -> bool:
        self.time = time.perf_counter() - self.start_perf_time
        self.start_perf_time = -1
        minutes = self.time / 60
        self.wpm = self.chars.correct_words / minutes
        self.avg_wpm = self.chars.correct_chars_avg / (self.time / 60)
        self.acc = (self.chars.correct_chars / self.chars.chars_count) * 100
        self.state = GameState.WINSCREEN
        self.print_status()
        while True:
            match self.stdscr.getch():
                case Key.r:
                    return True
                case Key.q:
                    break
        return False

    def _run_status_loop(self) -> None:
        self.status_thread_started = True
        while True:
            self.print_status()
            time.sleep(1)

    def print_status(self) -> None:
        _, max_x = self.status_win.getmaxyx()
        status_str = self.format_status()
        status_str = f"{status_str:<{max_x - 1}}"
        self.try_addnstr(self.status_win, 0, 0, status_str, max_x, self.status_color)
        self.status_win.refresh()

    def format_status(self) -> str:
        return self.status_fmt.format(
            correct=self.chars.correct_chars,
            wrong=self.chars.wrong_chars,
            left=self.chars.chars_count - self.chars.pos.current,
            time=self.time,
            wpm=self.wpm,
            avg_wpm=self.avg_wpm,
            acc=self.acc,
        )

    @property
    def status_fmt(self) -> str:
        match self.state:
            case GameState.TYPING:
                return self.chars_stats_fmt
            case GameState.WINSCREEN:
                return self.winscreen_status_fmt
            case _:
                return self.default_status_fmt


def main():
    args = parse_args()
    if args.words_file and args.words_file.exists():
        words_src = read_words_file(args.words_file)
    else:
        words_src = read_self_words()
    game = Game(words_src, args.words_count)
    try:
        curses.wrapper(game.run)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
