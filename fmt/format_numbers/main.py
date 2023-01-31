from textwrap import dedent
from argparse import ArgumentParser, Namespace
from typing import Tuple
from sys import exit, stderr


def parse_args(help=False) -> Namespace:
    parser = ArgumentParser(
        prog="numconverter",
        description="Shows input number in {dec}, {hex}, {oct} and {bin} bases".format(
            dec="\x1b[1mdec\x1b[0m", # bold
            hex="\x1b[1mhex\x1b[0m",
            oct="\x1b[1moct\x1b[0m",
            bin="\x1b[1mbin\x1b[0m",
        ),
    )

    parser.add_argument("default", help="input number")
    parser.add_argument(
        "-x", "--hex", action="store_true", default=False, help="accept input as hex"
    )
    parser.add_argument(
        "-o", "--oct", action="store_true", default=False, help="accept input as oct"
    )
    parser.add_argument(
        "-b", "--bin", action="store_true", default=False, help="accept input as bin"
    )

    if help:
        parser.print_help(stderr)
        exit(1)

    return parser.parse_args()


def parse_number(args: Namespace) -> Tuple[int, bool]:
    base = 10
    res = 0
    if args.hex:
        base = 16
    elif args.oct:
        base = 8
    elif args.bin:
        base = 2

    try:
        res = int(args.default, base)
    except Exception as e:
        print(f"\x1b[31;1m{repr(e)}\x1b[0m\n")
        parse_args(help=True)
        return res, False

    return res, True

def print_number(num: int):
    print(
        dedent(
            """
            hex: {0:x}
            int: {0}
            bin: {0:b}
            oct: {0:o}
        """.format(
                num
            )
        ).strip()
    )

def main():
    args = parse_args()

    num, ok = parse_number(args)
    if not ok:
        parse_args(help=True)
        exit(1)

    print_number(num)


if __name__ == "__main__":
    main()
