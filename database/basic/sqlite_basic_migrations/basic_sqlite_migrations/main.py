from .args import create_parser
from .db import init_db
from .logger import init_logger


def main():
    init_logger()
    args = create_parser().parse_args()
    init_db(filepath=args.filepath)


if __name__ == "__main__":
    main()
