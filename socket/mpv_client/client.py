import argparse
from contextlib import contextmanager
import json
import logging
from pathlib import Path
import socket
import subprocess as sp
import time
from typing import Dict, Optional


def init_logger(file: Optional[Path] = None):
    if not file:
        file = Path(__file__).resolve().parent.joinpath("client.log")
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(file)
    fh.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)",
            datefmt="%H:%M:%S %d/%m/%y",
        )
    )
    log.addHandler(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="mpv playlist-ctl concept script")
    parser.add_argument(
        "-f",
        "--file",
        default=Path("/tmp/mpv.sock"),
        type=Path,
        metavar="PATH",
        help="socket file (default: %(default)s)",
    )
    parser.add_argument(
        "-a", "--append", metavar="FILE", help="append file to the playlist"
    )
    parser.add_argument("-l", "--playlist", action="store_true", help="print playlist")
    parser.add_argument(
        "--log-file",
        type=Path,
        metavar="PATH",
        help="log file location for debugging purposes",
    )
    return parser.parse_args()


@contextmanager
def connect(file: Path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect(str(file))
        yield s
    except Exception as e:
        logging.fatal(repr(e))
        exit(1)
    finally:
        s.close()


def notify(msg: str) -> None:
    if not msg:
        return
    try:
        cmd = ["notify-send", "-i", "mpv", "-a", "mpv-client", msg]
        p = sp.run(cmd, stdout=sp.DEVNULL, stderr=sp.PIPE)
        if err := p.stderr.strip():
            logging.error("notify cmd return error: %r" % err)
    except Exception as e:
        logging.error(e)


class MpvClient:
    def __init__(self, socket_file: Path) -> None:
        self.socket_file = socket_file

    def playlist(self):
        with connect(self.socket_file) as sock:
            cmd = '{"command": ["get_property", "playlist"]}\n'
            logging.debug(cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                exit("can't read response")
            print("%r" % resp)

    def append(self, file: str):
        with connect(self.socket_file) as sock:
            cmd = '{ "command": ["loadfile", "%s", "append-play"] }\n' % file
            logging.debug("send %r" % cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                exit("can't read response")
            elif (err := resp.get("error")) != "success":
                exit("erdebugoccured: %r" % err)
            elif not (data := resp.get("data")):
                exit("invalid response: %r" % resp)

            msg = "entry with id %d just added" % data.get("playlist_entry_id", -1)
            logging.info(msg)
            notify(msg)

    def _read(self, conn: socket.socket) -> Optional[Dict]:
        data = b""
        try:
            while chunk := conn.recv(1024):
                data += chunk
                if chunk[-1] == 10 or len(chunk) < 1024:
                    break
            logging.debug("received data: %r" % data)
            return json.loads(data)
        except Exception as e:
            logging.error(e)


def check_mpv_process(file: Path):
    process_exists = lambda: sp.run(
        ["pidof", "mpv"],
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL,
    ).returncode
    try:
        if process_exists() != 0:
            cmd = "setsid -f mpv --idle --no-terminal --input-ipc-server=%s" % file
            logging.debug(cmd)
            p = sp.Popen(cmd.split(), stdout=sp.PIPE, stderr=sp.PIPE)
            _, err = p.communicate()
            if p.wait() != 0:
                raise Exception(err.decode())
            for _ in range(5):
                time.sleep(1)
                if process_exists():
                    break
            else:
                raise Exception("can't start mpv")
    except Exception as e:
        logging.error(e)
        exit("can't restart mpv")


if __name__ == "__main__":
    args = parse_args()
    init_logger(args.log_file)
    check_mpv_process(args.file)
    if not args.file.exists():
        exit("%s not found" % args.file)
    if not args.file.is_socket():
        exit("%s is not a socket file" % args.file)
    client = MpvClient(args.file)
    if args.append:
        client.append(args.append)
    elif args.playlist:
        client.playlist()
