import curses
from curses.textpad import rectangle as curses_rect
from enum import IntEnum
from functools import lru_cache
import random
import string
import threading
import time

valid_keys = set(map(ord, string.ascii_lowercase))
valid_chars = {" ", *string.ascii_lowercase}

words_count = 10

LOREM = "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis."
words = list(
    set(map(lambda w: w.lower(), LOREM.replace(",", "").replace(".", "").split()))
)

rnd_words = lambda: random.choices(words, k=words_count)


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


class CharsClass:
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
    def __init__(self, words: list[str]) -> None:
        self.words = words
        self.chars_class = CharsClass(self.words)
        self.start_perf_time = -1

        self.words_count = len(self.words)

        self.fg_yellow = 0
        self.fg_red = 0
        self.bg_white = 0
        self.status_color = 0

        self.status_fmt = " start typing..."
        self.in_game_stats = " correct: {correct} | wrong: {wrong} | left: {left}"

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
            if ch == 263:
                self.chars_class.move_backwards()
            elif ch in valid_keys:
                if self.start_perf_time < 0:
                    self.start_perf_time = time.perf_counter()
                    self.status_fmt = self.in_game_stats
                    self.print_status(status_win)

                self.chars_class.move_forward(chr(ch))

                if self.chars_class.pos.max == self.chars_class.pos.current:
                    curses.curs_set(0)
                    game_win.refresh()
                    self._run_winscreen_loop(stdscr, status_win)
                    return

            stdscr.refresh()

    def print_words_by_rows(self, game_win: "curses._CursesWindow") -> None:
        start_y, start_x = 2, 2
        y, x = start_y, start_x
        max_y, max_x = game_win.getmaxyx()
        pos = 0
        row_len = 0
        for word in self.chars_class.chars:
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
        if self.chars_class.pos.current == pos:
            color_pair = self.bg_white
        game_win.addnstr(y, x, char.char, 1, color_pair)

    def _run_winscreen_loop(
        self,
        stdscr: "curses._CursesWindow",
        status_win: "curses._CursesWindow",
    ) -> None:
        elapsed = time.perf_counter() - self.start_perf_time
        self.start_perf_time = -1
        wpm = 60 / elapsed * self.chars_class.correct_words
        acc = (self.chars_class.correct_chars / self.chars_class.chars_count) * 100
        stats = f"time: {elapsed:.1f}s | wpm: {wpm:.2f} | acc: {acc:.2f}%"
        self.status_fmt = f"{self.status_fmt} | {stats} | [r]: restart | [q]: quit"
        self.print_status(status_win)
        while True:
            ch = stdscr.getch()
            if ch == ord("r"):
                stdscr.refresh()
                self.__init__(rnd_words())
                self.run(stdscr)
                break
            elif ch == ord("q"):
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
            correct=self.chars_class.correct_chars,
            wrong=self.chars_class.wrong_chars,
            left=self.chars_class.chars_count - self.chars_class.pos.current,
        )


def main():
    game = Game(rnd_words())
    try:
        curses.wrapper(game.run)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    main()
