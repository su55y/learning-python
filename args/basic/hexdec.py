#!/usr/bin/env -S python3 -u

import argparse


def parse_agrs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hexdec")
    parser.add_argument("default", metavar="NUM", help="input number")
    parser.add_argument("-x", "--hex", action="store_true", help="accept input as hex")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__vesion__}",
    )
    return parser.parse_args()


def parse_num(v: str, base=10):
    try:
        return int(v, base)
    except ValueError as e:
        exit(e)


def main():
    args = parse_agrs()

    if args.hex:
        print(f"dec: {parse_num(args.default, 16)}")
    else:
        print(f"hex: {parse_num(args.default):x}")


__vesion__ = "1.3.37"

if __name__ == "__main__":
    main()
