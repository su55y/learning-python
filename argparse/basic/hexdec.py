import argparse
from sys import argv


def parse_agrs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="converts decimal numbers to hexadecimal and vice versa"
    )
    parser.add_argument("number", metavar="NUM", help="input number")
    parser.add_argument("-x", "--hex", action="store_true", help="accept input as hex")
    if not argv[1:]:
        parser.print_help()
        exit(1)
    return parser.parse_args()


def parse_num(v: str, hexbase: bool = False) -> str:
    try:
        fmt = "%d" if hexbase else "0x%02x"
        return fmt % int(v, 16 if hexbase else 10)
    except ValueError as e:
        return str(e)


if __name__ == "__main__":
    args = parse_agrs()
    print(parse_num(args.number, args.hex))
