import argparse
import re
import textwrap
from typing import Callable, List, Tuple
import sys


def validate_number(input: str):
    if not re.match(r"(^(0x)?[a-fA-F0-9]+$)|(^\d+$)", input):
        raise argparse.ArgumentTypeError(f"invalid number '{input}'")
    return input


def parse_args() -> Tuple[argparse.Namespace, Callable]:
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


def parse_numbers(args: argparse.Namespace) -> Tuple[List[int], Exception | None]:
    if not args.numbers or not isinstance(args.numbers, List):
        return [], Exception("invalid input numbers")

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


def print_numbers(nums: list[int]):
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


def main():
    args, print_help = parse_args()
    nums, err = parse_numbers(args)
    if err:
        print(f"\x1b[31;1m{repr(err)}\x1b[0m\n")
        print_help(sys.stdout)
        exit(1)

    print_numbers(nums)


if __name__ == "__main__":
    main()
