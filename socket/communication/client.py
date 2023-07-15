import argparse
from contextlib import contextmanager
from pathlib import Path
import socket
from time import sleep
from typing import Tuple


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


def send_cmd(cmd: str, file: Path, length=1024) -> Tuple[bytes, Exception | None]:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(str(file))
            s.sendall(cmd.encode())
            return s.recv(length), None
    except Exception as e:
        return b"", e


if __name__ == "__main__":
    args = parse_args()
    for _ in range(3):
        with connect(args.file) as sock:
            print("requesting time")
            sock.sendall(b"time")
            time = sock.recv(1024)
        print("time recieved: %r" % time.decode())
        sleep(1)
