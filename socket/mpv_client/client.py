import argparse
from contextlib import contextmanager
import json
import logging
from pathlib import Path
import socket
import subprocess as sp
import time
from typing import Dict, List, Optional

import requests


def init_logger(file: Optional[Path] = None) -> None:
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
    parser.add_argument("url", metavar="URL", help="append a video to the playlist")
    parser.add_argument(
        "-l",
        "--log-file",
        type=Path,
        metavar="PATH",
        help="log file location for debugging purposes",
    )
    parser.add_argument(
        "-s",
        "--socket-file",
        default=Path("/tmp/mpv.sock"),
        type=Path,
        metavar="PATH",
        help="socket file (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--playlist-file",
        default=Path("/tmp/mpv_playlist.json"),
        type=Path,
        metavar="PATH",
        help="mpv playlist state file (default: %(default)s)",
    )
    return parser.parse_args()


@contextmanager
def connect(file: Path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        s.connect(str(file))
        yield s
    except Exception as e:
        logging.critical(repr(e))
        exit(1)
    finally:
        s.close()


def notify(msg: str) -> None:
    try:
        p = sp.run(
            ["notify-send", "-i", "mpv", "-a", "mpv-client", msg],
            stdout=sp.DEVNULL,
            stderr=sp.PIPE,
        )
        if err := p.stderr.strip():
            logging.error("notify cmd return error: %r" % err)
    except Exception as e:
        logging.error(e)


def fetch_title(url: str) -> Optional[str]:
    try:
        resp = requests.get("https://youtube.com/oembed?url=%s&format=json" % url)
        logging.debug("%d %s %s" % (resp.status_code, resp.reason, resp.url))
        if resp.status_code == 200:
            return resp.json().get("title")
    except Exception as e:
        logging.error("can't fetch title for %r: %s" % (url, e))
        return url


class MpvClient:
    def __init__(self, socket_file: Path, playlist_file: Path) -> None:
        self.socket_file = socket_file
        self.playlist_file = playlist_file

    def append(self, file: str) -> None:
        with connect(self.socket_file) as sock:
            cmd = '{ "command": ["loadfile", "%s", "append-play"] }\n' % file
            logging.debug("send %r" % cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                logging.critical(msg := "can't read response")
                exit(msg)
            elif (err := resp.get("error")) != "success":
                logging.critical(err)
                exit(err)
            elif not (data := resp.get("data")):
                logging.critical(msg := "invalid response: %r" % resp)
                exit(msg)

            logging.info(
                msg := "entry with id %d just added" % data.get("playlist_entry_id", -1)
            )
            notify(msg)
            self.update_playlist()

    def update_playlist(self) -> None:
        mpv_playlist = self._playlist()
        playlist_storage = self._read_playlist() or {}
        for vid in mpv_playlist:
            url = vid.get("filename")
            if not url:
                logging.critical(
                    msg := "invalid playlist %r, filename missing for %r"
                    % (mpv_playlist, vid)
                )
                exit(msg)
            if url not in playlist_storage.keys():
                vid["title"] = fetch_title(url)
                logging.debug("new entry in playlist file: %r" % vid)
                if vid.get("playing"):
                    del vid["playing"]
                playlist_storage[url] = vid
            if vid.get("current") and not playlist_storage[url].get("current"):
                playlist_storage[url]["current"] = True
            elif not vid.get("current") and playlist_storage[url].get("current"):
                del playlist_storage[url]["current"]

        self._write_playlist(playlist_storage)

    def _playlist(self) -> List[Dict]:
        with connect(self.socket_file) as sock:
            cmd = '{"command": ["get_property", "playlist"]}\n'
            logging.debug(cmd)
            sock.sendall(cmd.encode())
            if not (resp := self._read(sock)):
                logging.critical(msg := "can't read response")
                exit(msg)
            if (err := resp.get("error")) != "success":
                logging.critical(err)
                exit(err)
            if (data := resp.get("data")) is None:
                logging.critical(msg := "data not found in resp: %r" % resp)
                exit(msg)
            return data

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

    def _read_playlist(self):
        if not self.playlist_file.exists():
            logging.info("creating new playlist file")
            return
        try:
            with open(self.playlist_file) as f:
                return json.load(f)
        except Exception as e:
            logging.critical(msg := "can't parse %r: %s" % (self.playlist_file, e))
            exit(msg)

    def _write_playlist(self, playlist: Dict):
        try:
            with open(self.playlist_file, "w") as f:
                logging.debug("updating %s" % self.playlist_file)
                json.dump(playlist, f)
        except Exception as e:
            logging.error(msg := "can't write to %r: %s" % (self.playlist_file, e))
            exit(msg)


def check_mpv_process(file: Path):
    process_exists = lambda: sp.run(["pidof", "-q", "mpv"]).returncode
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
    check_mpv_process(args.socket_file)
    if not args.socket_file.exists():
        exit("%s not found" % args.socket_file)
    if not args.socket_file.is_socket():
        exit("%s is not a socket file" % args.socket_file)
    MpvClient(args.socket_file, args.playlist_file).append(args.url)
