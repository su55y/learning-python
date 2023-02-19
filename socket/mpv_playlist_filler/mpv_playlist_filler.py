#!/usr/bin/env -S python3 -u

import subprocess as sp
import logging
import socket
import json
import re
import time
from os import path
from typing import Dict, List
from sys import argv

log: logging.Logger
silence = "-s" in argv[1:]

LOG_FMT = "[%(asctime)-.19s %(levelname)-.4s] %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"
SOCK_FILE = "/tmp/mpv.sock"
APP_LOG_FILE = "/tmp/mpv_playlist_filler.log"
APPEND_CMD = b"""{"command": ["loadfile", "%s", "append-play"]}\n"""
NOTIFY_SEND_CMD = ["notify-send", "-i", "mpv", "-a", "mpv"]
MPV_CMD = [
    "mpv",
    "--idle",
    f"--input-ipc-server={SOCK_FILE}",
    "--no-terminal",
    "--really-quiet",
]


def init_logger():
    global log
    log = logging.getLogger("gloabal_logger")
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(APP_LOG_FILE, mode="a")
    fh.setFormatter(logging.Formatter(LOG_FMT))
    log.addHandler(fh)
    if not silence:
        sh = logging.StreamHandler()
        sh.setFormatter(logging.Formatter(LOG_FMT))
        log.addHandler(sh)


def mpv_exists():
    try:
        out = sp.getoutput("pidof mpv")
    except Exception as e:
        log.warning(repr(e))
        return False
    else:
        return len(out) > 0


def start_mpv():
    log.info(f"starting mpv")
    try:
        p = sp.Popen(MPV_CMD)
        log.info(p.args)
    except Exception as e:
        log.error(repr(e))

    repeat = 0
    while not path.exists(SOCK_FILE) or repeat < 10:
        time.sleep(0.1)
        repeat += 1
    if not path.exists(SOCK_FILE):
        log.error(f"socket file {SOCK_FILE} not found")
        exit(1)


def notify_send(msg: str):
    NOTIFY_SEND_CMD.append(msg)
    try:
        sp.run(NOTIFY_SEND_CMD)
    except Exception as e:
        print(repr(e))


def send_cmd(cmd: bytes) -> List[Dict] | None:
    log.info(f"try cmd: {cmd}")
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCK_FILE)
            s.send(cmd)
            data = s.recv(2048)
            log.info(f"resp: {data}")
            data = data.decode("utf-8", "ignore").encode("utf-8")
            return json.loads(data.split(b"\n").pop(0))
    except Exception as e:
        log.error(repr(e))
        return None


def get_cb() -> str | None:
    try:
        out = sp.getoutput("xclip -o -selection clipboard")
    except Exception as e:
        log.error(repr(e))
    else:
        return out


def main():
    init_logger()

    if not mpv_exists():
        start_mpv()

    if (url := get_cb()) and re.match(
        r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$",
        url,
    ):
        if (resp := send_cmd(APPEND_CMD % url.encode())) and isinstance(resp, Dict):
            match resp.get("error"):
                case "success":
                    notify_send(f"appended {url}")
                case _:
                    notify_send(f"some error: {resp.get('error')}")
        else:
            notify_send(f"invalid cmd response")
            log.error(f"invalid cmd response ({resp})")


if __name__ == "__main__":
    main()
