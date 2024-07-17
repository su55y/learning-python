import string
import curses
import random

valid_keys = set(map(ord, string.ascii_lowercase))
words_count = 20

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
        if ch == 263:
            index = max(-1, index - 1)
        elif ch in valid_keys:
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
