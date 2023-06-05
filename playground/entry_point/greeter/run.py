from argparse import ArgumentParser
from getpass import getuser
from pkg_resources import require


def parse_args():
    parser = ArgumentParser(prog="greeter")
    try:
        version = require("greeter")[0].version
    except:
        version = "0.1"
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("-u", "--username", help="custom username")
    return parser.parse_args()


def greeting(username):
    print(f"hello {username}")


def main():
    args = parse_args()
    greeting(args.username or getuser())


if __name__ == "__main__":
    main()
