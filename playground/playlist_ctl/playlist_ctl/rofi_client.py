import logging
from threading import Thread

from playlist_ctl.storage import Storage
from playlist_ctl.mpv_client import MpvClient


class RofiClient:
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
                    Thread(target=self.stor.add_title, args=(url,)).start()
            print("%s\000info\037%d" % (title, i))
            if vid.get("current"):
                current = i
        print("\000active\037%d" % current)
