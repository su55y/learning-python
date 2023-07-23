import datetime as dt
import logging
from threading import Thread
from typing import Optional

import requests

from playlist_ctl.storage import Storage
from playlist_ctl.mpv_client import MpvClient


class PlaylistCtl:
    def __init__(self, stor: Storage, client: MpvClient) -> None:
        self.stor = stor
        self.client = client
        self.log = logging.getLogger()

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

    def add_title(self, url: str) -> None:
        if self.stor.select_title(url) is not None:
            return
        if (title := self._fetch_title(url)) is None:
            exit(1)
        created = str(dt.datetime.now(dt.timezone.utc))
        err = self.stor.insert_title((url, title, created))
        exit(0 if err is None else "can't insert title %s: %s" % (title, err))

    def _fetch_title(self, vid_url: str) -> Optional[str]:
        try:
            url = "https://youtube.com/oembed?url=%s&format=json" % vid_url
            resp = requests.get(url)
            self.log.debug("%d %s %s" % (resp.status_code, resp.reason, resp.url))
            if resp.status_code != 200:
                raise Exception(str(resp))
            return resp.json().get("title")
        except Exception as e:
            self.log.error("can't fetch title for %r: %s" % (vid_url, e))
