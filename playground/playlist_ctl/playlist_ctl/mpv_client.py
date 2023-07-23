from contextlib import contextmanager
import logging
import json
from pathlib import Path
import socket
from typing import Dict, List


class MpvClient:
    def __init__(self, file: Path) -> None:
        self.file = file
        self.log = logging.getLogger()

    @contextmanager
    def connect(self):
        if not self.file.exists():
            exit("%s not found" % self.file)
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(str(self.file))
            yield s
        except Exception as e:
            self.log.critical(repr(e))
            exit(1)
        finally:
            s.close()

    def mpv_playlist(self) -> List[Dict]:
        try:
            with self.connect() as sock:
                cmd = '{"command": ["get_property", "playlist"]}\n'
                self.log.debug(cmd)
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
                    self.log.critical(msg := "can't read response")
                    exit(msg)
                if (err := resp.get("error")) != "success":
                    self.log.critical(msg := "mpv error: %s" % err)
                    exit(msg)
                if (data := resp.get("data")) is None:
                    self.log.critical(msg := "data not found in resp: %r" % resp)
                    exit(msg)
                return data
        except Exception as e:
            self.log.critical(e)
            exit(str(e))
