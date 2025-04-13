import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="Database filepath")
    return parser
