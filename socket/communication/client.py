import argparse
from contextlib import contextmanager
from pathlib import Path
import socket
from time import sleep


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        default=Path("/tmp/test.sock"),
        type=Path,
        metavar="PATH",
        help="socket file (default: %(default)s)",
    )
    return parser.parse_args()


@contextmanager
def connect(file: Path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect(str(file))
        yield s
    except Exception as e:
        print(e)
    finally:
        s.close()


if __name__ == "__main__":
    args = parse_args()
    if not args.file.exists():
        exit("%s not found" % args.file)
    for _ in range(3):
        with connect(args.file) as sock:
            print("requesting time")
            sock.sendall(b"time")
            time = sock.recv(1024)
        print("time recieved: %r" % time.decode())
        sleep(1)
