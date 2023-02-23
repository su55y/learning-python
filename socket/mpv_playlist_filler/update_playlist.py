import socket
import json
from dataclasses import dataclass
from typing import Dict, List
from yt_dlp import YoutubeDL
from re import match


@dataclass
class PlaylistItem:
    id: int
    filename: str
    current: bool | None = None
    playing: bool | None = None


@dataclass
class MpvResponse:
    request_id: int
    error: str
    data: List[PlaylistItem]


RX_URL = r".*youtube\.com\/watch\?v=([\w\d_\-]{11})|.*youtu\.be\/([\w\d_\-]{11})|.*twitch\.tv\/videos\/(\d{10})$"
CMD_GET_PLAYLIST = b"""{"command": ["get_property", "playlist"]}\n"""
PLAYLIST_FILE = "/tmp/mpv_current_playlist"


def send_cmd(cmd: bytes) -> Dict | None:
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect("/tmp/mpv.sock")
            s.send(cmd)
            data = s.recv(2**14)
            return json.loads(data)
    except Exception as e:
        print(repr(e))


def parse_response(resp: Dict) -> MpvResponse | None:
    try:
        if base := MpvResponse(**resp):
            if base and base.data and isinstance(base.data, List):
                base.data = [
                    PlaylistItem(**item) for item in base.data if isinstance(item, Dict)
                ]
            return base
    except Exception as e:
        print(repr(e))


def get_title(url: str) -> str:
    with YoutubeDL({"quiet": True}) as yt_dl:
        if not (info := yt_dl.extract_info(url, download=False)):
            return url
        else:
            return info.pop("title") or url


def update_playlist_file(playlist: List[str]):
    try:
        with open(PLAYLIST_FILE, "w") as f:
            f.write("\n".join(playlist))
    except Exception as e:
        print(repr(e))


def update_playlist():
    if raw_resp := send_cmd(CMD_GET_PLAYLIST):
        if mpv_resp := parse_response(raw_resp):
            playlist = []
            for i, v in enumerate(mpv_resp.data):
                title = (
                    get_title(v.filename) if match(RX_URL, v.filename) else v.filename
                )
                playlist.append(f"{i} {title}")
            if playlist:
                update_playlist_file(playlist)
