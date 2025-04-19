import curses
from pathlib import Path
import re
import tomllib

PALETTES_DIR = Path(__file__).with_name("palettes")
if not PALETTES_DIR.exists() or not PALETTES_DIR.is_dir():
    print("palettes dir not found")
    exit(1)


rx_hex_color_6 = re.compile(r"^\#[a-f0-9]{6}$")
rx_hex_color_3 = re.compile(r"^\#[a-f0-9]{3}$")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    if rx_hex_color_6.match(h):
        return int(h[1:3], base=16), int(h[3:5], base=16), int(h[5:7], base=16)
    if rx_hex_color_3.match(h):
        return int(h[1], base=16), int(h[2], base=16), int(h[3], base=16)
    raise ValueError(f"Invalid hex color {h!r}")


def rgb_to_curses_rgb(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = tuple(int(round(1000 * c / 255)) for c in rgb)
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
    curses.curs_set(0)
    if not curses.can_change_color():
        raise Exception("Can't change color =(")

    palettes_map = get_palettes_map()
    for palette in palettes_map.values():
        for color_set in palette.values():
            for color in color_set.values():
                curses.init_color(color["index"], *color["rgb"])
                curses.init_pair(color["index"], 0, color["index"])

    order = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

    def draw():
        s.clear()
        for name, p in palettes_map.items():
            s.addstr(f"{name}\n", curses.A_BOLD)
            for k in order:
                s.addstr("   ", curses.color_pair(p["normal"][k]["index"]))
            s.addstr("\n")
            for k in order:
                s.addstr("   ", curses.color_pair(p["bright"][k]["index"]))
            s.addstr("\n")

    while True:
        try:
            draw()
        except curses.error:
            pass
        try:
            ch = s.getch()
            if ch == ord("q"):
                break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    curses.wrapper(run)
