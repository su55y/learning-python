import curses
from pathlib import Path
import re
import sys
import tomllib

PALETTES_DIR = Path(__file__).with_name("palettes")
if not PALETTES_DIR.exists() or not PALETTES_DIR.is_dir():
    print("palettes dir not found")
    exit(1)


rx_hex_color_6 = re.compile(r"^\#[a-f0-9]{6}$")
rx_hex_color_3 = re.compile(r"^\#[a-f0-9]{3}$")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lower()
    if rx_hex_color_6.match(h):
        return int(h[1:3], base=16), int(h[3:5], base=16), int(h[5:7], base=16)
    if rx_hex_color_3.match(h):
        return int(h[1], base=16), int(h[2], base=16), int(h[3], base=16)
    raise ValueError(f"Invalid hex color {h!r}")


def rgb_to_curses_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = tuple(1000 * c // 255 for c in rgb)
    return r, g, b


def read_palette(filepath: Path) -> dict:
    with open(filepath, "rb") as f:
        return tomllib.load(f)


def get_palettes_map() -> dict[str, dict]:
    palettes = {}
    color_index = 17
    for palette_path in PALETTES_DIR.glob("*.toml"):
        palette = read_palette(PALETTES_DIR / palette_path)
        indexed_palette = {}
        for k, colorset in palette.items():
            indexed_palette[k] = {}
            for name, color in colorset.items():
                crgb = rgb_to_curses_rgb(hex_to_rgb(color))
                indexed_palette[k][name] = {
                    "index": color_index,
                    "hex": color,
                    "rgb": crgb,
                }
                color_index += 1
                assert color_index < 256, "colors limit exceeded"

        palettes[palette_path.name.removesuffix(".toml")] = indexed_palette
    return palettes


def run(s: "curses._CursesWindow"):
    if not curses.has_colors() or curses.COLORS < 256:
        raise NotImplementedError("TERM should be xterm-256color")
    if not curses.can_change_color():
        raise NotImplementedError("Can't change color =(")

    curses.curs_set(0)
    curses.use_default_colors()

    order = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    for i in range(16):
        curses.init_pair(i, 0, i)

    palettes_map = get_palettes_map()
    for palette in palettes_map.values():
        for color_set in palette.values():
            for color in color_set.values():
                curses.init_color(color["index"], *color["rgb"])
                curses.init_pair(color["index"], 0, color["index"])

    max_y, max_x = s.getmaxyx()
    pad_pos = 0
    pad_size = 3 + (3 * len(palettes_map))
    pad = curses.newpad(pad_size + 1, max_x)

    pad.addstr("Default\n", curses.A_BOLD)
    for i in range(16):
        pad.addstr("   ", curses.color_pair(i))
        if (i + 1) % 8 == 0:
            pad.addstr("\n")
    for name, p in palettes_map.items():
        pad.addstr(f"{name}\n", curses.A_BOLD)
        for k in order:
            pad.addstr("   ", curses.color_pair(p["normal"][k]["index"]))
        pad.addstr("\n")
        for k in order:
            pad.addstr("   ", curses.color_pair(p["bright"][k]["index"]))
        pad.addstr("\n")

    pad.refresh(pad_pos, 0, 0, 0, max_y - 1, max_x - 1)
    s.refresh()

    while True:
        max_y, max_x = s.getmaxyx()
        pad.refresh(pad_pos, 0, 0, 0, max_y - 1, max_x - 1)
        ch = s.getch()
        if ch == ord("q"):
            break
        elif ch in (ord("j"), curses.KEY_DOWN):
            pad_pos = min(pad_pos + 1, pad.getyx()[0] - max_y)
        elif ch in (ord("k"), curses.KEY_UP):
            pad_pos = max(0, pad_pos - 1)
        elif ch in (ord("g"), curses.KEY_HOME):
            pad_pos = 0
        elif ch in (ord("G"), curses.KEY_END):
            pad_pos = max(pad_size - max_y, 0)
        s.refresh()
    return 0


def main():
    try:
        return curses.wrapper(run)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        raise e


if __name__ == "__main__":
    sys.exit(main())
