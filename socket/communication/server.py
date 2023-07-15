import argparse
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import re
import socket
import signal

COMMAND_LIST = """command list:
    time        returns current time
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        epilog=COMMAND_LIST,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
def server_socket(file: Path):
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        server_socket.bind(str(file))
        server_socket.listen(1)
        print("listening at %s....." % file)

        yield server_socket
    except Exception as e:
        print(e)
    finally:
        server_socket.close()
        print("socket closed, removing %s" % file)
        file.unlink()


def signal_handler(*_):
    print("shutting down...")
    raise SystemExit(0)


def handle_cmd(cmd: str) -> bytes:
    match cmd:
        case "time":
            print("time cmd handled")
            return datetime.now().strftime("%H:%M:%S").encode()
        case _:
            unkwown = "unkwown cmd {!r}".format(cmd[:10])
            print(unkwown)
            return unkwown.encode()


if __name__ == "__main__":
    args = parse_args()
    if args.file.exists():
        yes = input("%s already exists, remove? [y]") or "y"
        args.file.unlink() if re.match("^[yY].*", yes) else exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    with server_socket(args.file) as s:
        while True:
            conn, _ = s.accept()
            try:
                resp = handle_cmd(conn.recv(2048).decode())
                conn.sendall(resp)
            except Exception as e:
                print(e)
            finally:
                conn.close()
