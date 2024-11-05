from pathlib import Path
import toml

palettes_dir = Path(__file__).parent / "palettes"
if not palettes_dir.exists():
    print("palettes dir not found")
    exit(1)


def hex_to_rgb(v: str) -> tuple[int, int, int]:
    if len(v) != 7:
        raise ValueError(f"Invalid hex value {v!r}")
    return int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)


def print_color(color: str):
    r, g, b = hex_to_rgb(color)
    print(f"\033[48;2;{r};{g};{b}m   ", end="\033[0m ")


def print_palette(palette: dict):
    for colors in palette.values():
        for color in colors.values():
            print_color(color)
        print()


def read_palette(path) -> dict:
    with open(palettes_dir / path) as f:
        return toml.load(f)


if __name__ == "__main__":
    for palette_path in palettes_dir.glob("*.toml"):
        palette = read_palette(palette_path)
        print(f"\033[1;38m{palette_path.name.removesuffix('.toml')}\033[0m")
        print_palette(palette)
        print()
