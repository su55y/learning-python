import argparse
from contextlib import contextmanager
import json
import logging
from pathlib import Path
import socket
import subprocess as sp
import time
from typing import Dict, List, Optional


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
    parser.add_argument(
        "-p",
        "--playlist-file",
        default=Path("/tmp/mpv_playlist.json"),
        type=Path,
        metavar="PATH",
        help="playlist state file (%(default)s)",
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


def fetch_title(url: str) -> str:
    try:
        return sp.getoutput("yt-dlp -e %s" % url)
    except Exception as e:
        logging.error("can't fetch title for %r: %s" % (url, e))
        return url


class MpvClient:
    def __init__(self, socket_file: Path, playlist_file: Path) -> None:
        self.socket_file = socket_file
        self.playlist_file = playlist_file

    def playlist(self) -> List[Dict]:
        with connect(self.socket_file) as sock:
            cmd = '{"command": ["get_property", "playlist"]}\n'
            logging.debug(cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                exit("can't read response")
            if (err := resp.get("error")) != "success":
                exit(err)
            if (data := resp.get("data")) is None:
                exit("data not found in resp: %r" % resp)
            return data

    def append(self, file: str) -> None:
        with connect(self.socket_file) as sock:
            cmd = '{ "command": ["loadfile", "%s", "append-play"] }\n' % file
            logging.debug("send %r" % cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                exit("can't read response")
            elif (err := resp.get("error")) != "success":
                exit(err)
            elif not (data := resp.get("data")):
                exit("invalid response: %r" % resp)

            msg = "entry with id %d just added" % data.get("playlist_entry_id", -1)
            logging.info(msg)
            notify(msg)
            self.update_playlist()

    def update_playlist(self) -> None:
        mpv_playlist = self.playlist()
        playlist_storage = {}
        if self.playlist_file.exists():
            with open(self.playlist_file) as f:
                playlist_storage = json.load(f)
        for vid in mpv_playlist:
            if (url := vid.get("filename")) not in playlist_storage.keys():
                if not url:
                    logging.error(
                        "invalid playlist %r, filename missing for %r"
                        % (mpv_playlist, vid)
                    )
                    continue
                vid["title"] = fetch_title(url)
                logging.debug("new entry in playlist file: %r" % vid)
                playlist_storage[url] = vid
        with open(self.playlist_file, "w") as f:
            json.dump(playlist_storage, f)

    def _read(self, conn: socket.socket) -> Optional[Dict]:
        data = b""
        try:
            while chunk := conn.recv(1024):
                data += chunk
                if chunk[-1] == 10 or len(chunk) < 1024:
                    break
            logging.debug("received data: %r" % data)
            for raw_part in data.decode().split():
                part = json.loads(raw_part)
                if "event" in part.keys():
                    continue
                return part
        except Exception as e:
            logging.error(e)


def check_mpv_process(file: Path):
    process_exists = lambda: sp.run(
        ["pidof", "mpv"],
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL,
    ).returncode
    try:
        if process_exists() == 0:
            return
        cmd = "setsid -f mpv --idle --no-terminal --input-ipc-server=%s" % file
        logging.debug(cmd)
        p = sp.Popen(cmd.split(), stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        if (code := p.wait()) != 0:
            raise Exception("setsid return status code: %d" % code)
        for _ in range(10):
            time.sleep(0.5)
            if process_exists() == 0:
                break
        else:
            raise Exception("waiting process timeout")
    except Exception as e:
        logging.error(e)
        exit("can't start mpv")


if __name__ == "__main__":
    args = parse_args()
    init_logger(args.log_file)
    check_mpv_process(args.file)
    if not args.file.exists():
        exit("%s not found" % args.file)
    if not args.file.is_socket():
        exit("%s is not a socket file" % args.file)
    client = MpvClient(args.file, args.playlist_file)
    if args.append:
        client.append(args.append)
    # TODO: print formatted for rofi playlist
    elif args.playlist:
        client.playlist()
