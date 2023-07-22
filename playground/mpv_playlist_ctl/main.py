import argparse
from contextlib import contextmanager
import datetime as dt
import json
import logging
from pathlib import Path
import requests
import socket
import sqlite3
from threading import Thread
from typing import Dict, List, Optional, Tuple


def init_logger() -> None:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler("main.log")
    fh.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)",
            datefmt="%H:%M:%S %d/%m/%y",
        )
    )
    log.addHandler(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", metavar="URL", help="add new title")
    parser.add_argument(
        "-s",
        "--socket",
        metavar="PATH",
        default=Path("/tmp/mpv.sock"),
        help="socket file (default: %(default)s)",
    )
    return parser.parse_args()


def fetch_title(vid_url: str) -> Optional[str]:
    try:
        url = "https://youtube.com/oembed?url=%s&format=json" % vid_url
        resp = requests.get(url)
        logging.debug("%d %s %s" % (resp.status_code, resp.reason, resp.url))
        if resp.status_code != 200:
            raise Exception(str(resp))
        return resp.json().get("title")
    except Exception as e:
        logging.error("can't fetch title for %r: %s" % (vid_url, e))


class Storage:
    def __init__(self, file: Path) -> None:
        self.file = file

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(str(self.file))
        try:
            cursor = conn.cursor()
            yield cursor
        except Exception as e:
            logging.critical(e)
        else:
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> Optional[Exception]:
        titles_schema = """CREATE TABLE IF NOT EXISTS titles (
        url TEXT PRIMARY KEY NOT NULL,
        title TEXT NOT NULL,
        created DATETIME NOT NULL)"""
        try:
            with self.get_cursor() as cur:
                cur.execute(titles_schema)
        except Exception as e:
            return e

    def insert_title(self, title: Tuple[str, str, str]) -> Optional[Exception]:
        query = "INSERT OR IGNORE INTO titles (url, title, created) VALUES (?, ?, ?)"
        try:
            with self.get_cursor() as cur:
                logging.debug("%s: %s" % (query, title))
                cur.execute(query, title)
        except Exception as e:
            logging.error(e)
            return e

    def select_title(self, url: str) -> Optional[str]:
        try:
            with self.get_cursor() as cur:
                cur.execute("SELECT title FROM titles WHERE url = ? LIMIT 1", (url,))
                title, *_ = row if (row := cur.fetchone()) else (None,)
                return title
        except Exception as e:
            logging.error(e)

    def select_titles(self, urls: str) -> Dict[str, str]:
        try:
            with self.get_cursor() as cur:
                q = "SELECT url, title FROM titles WHERE url in (%s)" % urls
                logging.debug(q)
                cur.execute(q)
                return {url: title for url, title in cur.fetchall()}
        except Exception as e:
            logging.error("can't select titles: %s" % e)
            return {}


class MpvClient:
    def __init__(self, file: Path) -> None:
        self.file = file

    @contextmanager
    def connect(self):
        if not self.file.exists():
            exit("%s not found" % self.file)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(str(self.file))
            yield s
        except Exception as e:
            logging.critical(repr(e))
            exit(1)
        finally:
            s.close()

    def mpv_playlist(self) -> List[Dict]:
        try:
            with self.connect() as sock:
                cmd = '{"command": ["get_property", "playlist"]}\n'
                logging.debug(cmd)
                sock.sendall(cmd.encode())
                data = b""
                while chunk := sock.recv(1024):
                    data += chunk
                    if chunk[-1] == 10 or len(chunk) < 1024:
                        break

                resp = None
                for raw_part in data.decode().split():
                    part = json.loads(raw_part)
                    if "event" in part.keys():
                        continue
                    resp = part
                if not resp:
                    logging.critical(msg := "can't read response")
                    exit(msg)
                if (err := resp.get("error")) != "success":
                    logging.critical(msg := "mpv error: %s" % err)
                    exit(msg)
                if (data := resp.get("data")) is None:
                    logging.critical(msg := "data not found in resp: %r" % resp)
                    exit(msg)
                return data
        except Exception as e:
            logging.critical(e)
            exit(str(e))


class PlaylistCtl:
    def __init__(self, stor: Storage, client: MpvClient) -> None:
        self.stor = stor
        self.client = client

    def add_title(self, url: str) -> None:
        if (title := fetch_title(url)) is None:
            exit(1)
        created = str(dt.datetime.now(dt.timezone.utc))
        err = self.stor.insert_title((url, title, created))
        exit(0 if err is None else "can't insert title %s: %s" % (title, err))

    def print_playlist(self):
        playlist = self.client.mpv_playlist()
        urls = ", ".join("%r" % v.get("filename", "-") for v in playlist)
        titles = self.stor.select_titles(urls)
        current = 0
        for i, vid in enumerate(playlist):
            if (url := vid.get("filename")) is None:
                title = "unknown %d" % i
            else:
                if (title := titles.get(url)) is None:
                    title = url
                    Thread(target=self.add_title, args=(url,)).start()
            print("%s\000info\037%d" % (title, i))
            if vid.get("current"):
                current = i
        print("\000active\037%d" % current)


if __name__ == "__main__":
    args = parse_args()
    init_logger()

    stor = Storage(Path("cache.db"))
    if err := stor.init_db():
        exit("can't create table: %s" % err)

    ctl = PlaylistCtl(stor, MpvClient(args.socket))
    if args.add:
        if stor.select_title(args.add) is not None:
            exit(0)
        ctl.add_title(args.add)
    else:
        ctl.print_playlist()
