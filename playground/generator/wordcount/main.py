import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        type=Path,
        default=Path(__file__),
        nargs="?",
        help="file to count words (default: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    count = 0
    reader = (row for row in open(args.file))
    for row in reader:
        if row := row.strip():
            count += len(row.split())
    print(count)
