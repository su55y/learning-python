import string
import curses
import random

valid_keys = set(map(ord, string.ascii_lowercase))
words_count = 10

LOREM = "Lorem ipsum dolor sit amet, officia excepteur ex fugiat reprehenderit enim labore culpa sint ad nisi Lorem pariatur mollit ex esse exercitation amet. Nisi anim cupidatat excepteur officia. Reprehenderit nostrud nostrud ipsum Lorem est aliquip amet voluptate voluptate dolor minim nulla est proident. Nostrud officia pariatur ut officia. Sit irure elit esse ea nulla sunt ex occaecat reprehenderit commodo officia dolor Lorem duis laboris cupidatat officia voluptate. Culpa proident adipisicing id nulla nisi laboris ex in Lorem sunt duis officia eiusmod. Aliqua reprehenderit commodo ex non excepteur duis sunt velit enim. Voluptate laboris sint cupidatat ullamco ut ea consectetur et est culpa et culpa duis."
words = list(
    set(map(lambda w: w.lower(), LOREM.replace(",", "").replace(".", "").split()))
)

rnd_words = lambda: random.choices(words, k=words_count)
words_len = lambda words_: len(" ".join(words_))


def main(stdscr: "curses._CursesWindow"):
    curses.use_default_colors()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_YELLOW, 0)
    fg_yellow = curses.color_pair(1)
    raw_game_words = rnd_words()
    game_words_str = " ".join(raw_game_words)
    # game_words_len = words_len(game_words)
    game_words_len = len(game_words_str)
    index = -1

    max_y, max_x = stdscr.getmaxyx()

    def print_words() -> None:
        my, mx = stdscr.getmaxyx()
        y = 0
        color_pair = 0
        for x, ch in enumerate(game_words_str):
            if x + 1 == mx:
                y += 1
            if y + x <= index:
                color_pair = fg_yellow
            else:
                color_pair = 0
            stdscr.addnstr(y, x, ch, 1, color_pair)

    print_words()
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch == 263:
            index = max(-1, index - 1)
        else:
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
