from enum import IntEnum
from functools import lru_cache
import string
import curses
import random

valid_keys = set(map(ord, string.ascii_lowercase))
valid_keys.add(ord(" "))
valid_chars = {" ", *string.ascii_lowercase}

words_count = 20

LOREM = "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis."
words = list(
    set(map(lambda w: w.lower(), LOREM.replace(",", "").replace(".", "").split()))
)

rnd_words = lambda: random.choices(words, k=words_count)
words_len = lambda words_: len(" ".join(words_))


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
        self.max = max(0, length - 1)
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


class TextChunk:
    def __init__(self, chars: str, state: CharState) -> None:
        self.state = state
        self.chars = chars


class TextProducer:
    def __init__(self, game_words: list[str]) -> None:
        assert len(game_words) > 0
        self.words = game_words
        self.chars_ = self.build_chars_alt(self.words)
        self.chars = self.build_chars(self.words)
        # self.pos = CursorPos(length=len(self.chars))
        self.chars_count = sum(map(len, game_words))
        self.pos = CursorPos(length=sum(map(len, game_words)))

    def update_char(self, char: str) -> bool:
        pos = 0
        for i in range(len(self.chars_)):
            for j in range(len(self.chars_[i])):
                if pos == self.pos.current:
                    self.chars_[i][j].input = char
                    return True
                pos += 1
        print(f"can't increment with {char!r}")
        return False

    def move_forward(self, char: str) -> None:
        # if not self.pos.is_increment_valid:
        #     return
        # self.chars[self.pos.current].input = char
        # self.chars_[self.pos.current].input = char
        if self.update_char(char):
            self.pos.increment()
        # self.check_if_next_space()

    def check_if_next_space(self) -> None:
        if self.chars[self.pos.current].char == " ":
            self.pos.increment()

    def check_if_prev_space(self) -> None:
        if not self.pos.is_decrement_valid:
            return
        if self.chars[self.pos.current].char == " ":
            self.pos.decrement()

    def move_backwards(self) -> None:
        if not self.pos.is_decrement_valid:
            return
        if self.pos.current > 0:
            self.pos.decrement()
        if not self.update_char(""):
            self.pos.increment()
        # self.chars[self.pos.current].input = ""
        # self.check_if_prev_space()

    def produce_text_alt(self) -> list[TextChunk]:
        text: list[TextChunk] = list()
        i = 0
        while i < len(self.chars_):
            word = self.chars_[i]
            j = 0
            while j < len(word):
                # for j in range(len(self.chars_[i])):
                chunk_text = ""
                chunk_state = self.chars_[i][j].state
                while j < len(word) and chunk_state == self.chars_[i][j].state:
                    chunk_text += self.chars_[i][j].char
                    j += 1
                if len(chunk_text):
                    text.append(TextChunk(chunk_text, chunk_state))
            text.append(TextChunk(" ", CharState.Default))
            i += 1
        return text

    def produce_text(self) -> list[TextChunk]:
        text: list[TextChunk] = list()
        i = 0
        while i < len(self.chars):
            chunk_text = ""
            chunk_state = self.chars[i].state
            while i < len(self.chars) and chunk_state == self.chars[i].state:
                chunk_text += self.chars[i].char
                i += 1
            if len(chunk_text):
                text.append(TextChunk(chunk_text, chunk_state))

        return text

    @staticmethod
    def build_chars_alt(words_: list[str]) -> list[list[Char]]:
        chars: list[list[Char]] = list()
        for word in words_:
            chars.append(list(map(Char, word)))
        return chars

    @staticmethod
    def build_chars(words_: list[str]) -> list[Char]:
        chars: list[Char] = list()
        for word in words_:
            chars.extend(map(Char, word))
        return chars


def main(stdscr: "curses._CursesWindow"):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    curses.init_pair(2, curses.COLOR_RED, 0)
    curses.init_pair(3, 0, curses.COLOR_YELLOW)
    curses.init_pair(4, 0, curses.COLOR_RED)
    curses.init_pair(5, 0, curses.COLOR_WHITE)
    fg_yellow = curses.color_pair(1)
    fg_red = curses.color_pair(2)
    bg_yellow = curses.color_pair(3)
    bg_red = curses.color_pair(4)
    bg_white = curses.color_pair(5)

    raw_game_words = rnd_words()
    game_words_str = " ".join(raw_game_words)
    # game_words_len = words_len(game_words)
    game_words_len = len(game_words_str)
    index = -1
    tp = TextProducer(raw_game_words)

    max_y, max_x = stdscr.getmaxyx()

    def words_by_rows(mx) -> list[list[str]]:
        rows = [[]]
        i = 0
        for word in raw_game_words:
            l = len("".join(rows[i])) + len(rows[i]) + len(word)
            if l >= mx:
                i += 1
                rows.append([word])
            else:
                rows[i].append(word)
        return rows

    def print_words() -> None:
        stdscr.clear()
        color_pair = 0
        pos = 0
        for word in tp.chars_:
            for char in word:
                color_pair = 0
                if char.state == CharState.Correct:
                    color_pair = fg_yellow
                elif char.state == CharState.Wrong:
                    color_pair = fg_red
                if tp.pos.current == pos:
                    color_pair = bg_white
                stdscr.addnstr(char.char, 1, color_pair)
                pos += 1
            stdscr.addnstr(" ", 1, 0)

    def print_words_() -> None:
        my, mx = stdscr.getmaxyx()
        color_pair = 0
        rows = words_by_rows(mx)
        char_index = 0
        for y, row in enumerate(rows):
            x = 0
            for _, word in enumerate(row):
                for i, ch in enumerate(word):
                    if char_index <= index:
                        color_pair = fg_yellow
                    else:
                        color_pair = 0
                    try:
                        stdscr.addnstr(y, x, ch, 1, color_pair)
                    except:
                        pass
                    x += 1
                    char_index += 1
                try:
                    stdscr.addnstr(y, x, " ", 1)
                except:
                    pass
                x += 1
                char_index += 1
            stdscr.refresh()

    print_words()
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ord(" ") == ch:
            continue
        if ch == 263:
            tp.move_backwards()
            index = max(-1, index - 1)
        elif ch in valid_keys:
            tp.move_forward(chr(ch))
            index += 1
        # stdscr.clrtoeol()
        print_words()
        stdscr.refresh()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"ERR: {e}")
