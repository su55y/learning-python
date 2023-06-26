import argparse
import re
import textwrap
from typing import Callable, List, Tuple, Optional


def parse_args() -> Tuple[argparse.Namespace, Callable]:
    def validate_number(input: str) -> str:
        if not re.match(r"^((?:0[xob])?[a-fA-F0-9]+$)|(^\d+$)", input):
            raise argparse.ArgumentTypeError(f"invalid number '{input}'")
        return input

    parser = argparse.ArgumentParser(
        prog="numconverter",
        description="Shows input number in {dec}, {hex}, {oct} and {bin} bases".format(
            dec="\x1b[1mdec\x1b[0m",
            hex="\x1b[1mhex\x1b[0m",
            oct="\x1b[1moct\x1b[0m",
            bin="\x1b[1mbin\x1b[0m",
        ),
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=validate_number,
        metavar="NUM",
        help="input numbers",
    )
    parser.add_argument("-x", "--hex", action="store_true", help="accept input as hex")
    parser.add_argument("-o", "--oct", action="store_true", help="accept input as oct")
    parser.add_argument("-b", "--bin", action="store_true", help="accept input as bin")

    return parser.parse_args(), parser.print_help


def parse_numbers(args: argparse.Namespace) -> Tuple[List[int], Optional[Exception]]:
    base = 10
    match True:
        case args.hex:
            base = 16
        case args.oct:
            base = 8
        case args.bin:
            base = 2

    try:
        return [int(n, base) for n in args.numbers], None
    except Exception as e:
        return [], e


if __name__ == "__main__":
    args, print_help = parse_args()
    nums, err = parse_numbers(args)
    if err:
        print(f"\x1b[31;1m{err}\x1b[0m\n")
        print_help()
        exit(1)

    print(
        textwrap.dedent(
            """
            dec: {dec}
            hex: {hex}
            bin: {bin}
            oct: {oct}
        """.format(
                dec=", ".join([f"{n}" for n in nums]),
                hex=", ".join([f"{n:x}" for n in nums]),
                bin=", ".join([f"{n:b}" for n in nums]),
                oct=", ".join([f"{n:o}" for n in nums]),
            )
        ).strip()
    )
