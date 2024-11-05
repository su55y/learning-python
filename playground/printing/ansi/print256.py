# Tom Hale, 2016. MIT Licence.
# Print out 256 colours, with each number printed in its corresponding colour
# See http://askubuntu.com/questions/821157/print-a-256-color-test-pattern-in-the-terminal/821163#821163


def get_contrast(color: int) -> int:
    if color == 0:
        return 15

    if color < 16:
        return 0

    if color > 231:
        return 15 if color < 244 else 0

    r = (color - 16) / 36
    g = ((color - 16) % 36) / 6
    b = (color - 16) % 6
    luminance = (r * 299) + (g * 587) + (b * 114)
    return 0 if luminance > 2500 else 15


def print_color(color: int):
    contrast = get_contrast(color)
    print(f"\033[48;5;{color}m", end="")
    print(f"\033[38;5;{contrast}m{color:3d}", end="\033[0m ")


def print_colors_range(start: int, colors_count: int):
    for i in range(start, min(start + colors_count, 255)):
        print_color(i)


def print_blocks(
    start: int,
    end: int,
    block_cols: int,
    block_rows: int,
    blocks_per_line: int,
):
    block_length = block_cols * block_rows
    i = start
    while i <= end:
        print()
        for _ in range(block_rows):
            for block in range(blocks_per_line):
                print_colors_range(i + (block * block_length), block_cols)
                print("  ", end="")
            i += block_cols
            print()
        i += (blocks_per_line - 1) * block_length


if __name__ == "__main__":
    print_blocks(0, 15, 8, 2, 1)
    print_blocks(16, 231, 6, 6, 3)
    print_blocks(232, 255, 12, 2, 1)
