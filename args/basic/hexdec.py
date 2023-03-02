#!/usr/bin/env -S python3 -u

import argparse
from sys import exit


def parse_agrs():
    parser = argparse.ArgumentParser(
        prog="hexdec",
        description="Hex-Dec Base Converter",
        epilog="more params: docs.python.org/3/library/argparse.html#argumentparser-objects",
    )
    parser.add_argument("default", nargs="?", help="input number")
    parser.add_argument(
        "-H", "--hex", action="store_true", default=False, help="accept input as hex"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=(f"%(prog)s {__vesion__}")
    )
    return parser.parse_args()


def main():
    try:
        args = parse_agrs()
    except Exception as e:
        print(f"can't parse args: '{repr(e)}'")
        exit(1)

    input = args.default

    if not input:
        print("input not given")
        exit(1)

    if args.hex:
        try:
            print(f"dec: {int(input, 16)}")
        except:
            print(f"can't convert hex '{input}' to int")
            exit(1)
        exit(0)

    try:
        print(f"hex: {hex(int(input, 10))}")
    except ValueError:
        try:
            print(f"dec: {int(input, 16)}")
        except:
            print(f"can't determine type of '{input}'")
    except TypeError as e:
        print(e)
    except:
        print(f"can't determine type of '{input}'")


__vesion__ = "1.3.37"

if __name__ == "__main__":
    main()
