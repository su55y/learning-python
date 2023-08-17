import argparse
from collections.abc import Callable
from http import HTTPStatus
import http.server
import json
import gzip
import logging as log
import mimetypes
from pathlib import Path
import socketserver
import sys
import time
import threading
from typing import Optional

PORT = 8000
STATIC_DIR = Path(__file__).parent.joinpath("static")
CACHE = {}

log.basicConfig(
    level=log.DEBUG,
    format="%(asctime)s %(levelname)s] %(message)s (%(filename)s:%(lineno)d)",
    datefmt="%H:%M:%S",
)


def get_static_file(path) -> bytes | None:
    try:
        log.debug("opening static: %s" % path)
        with open(STATIC_DIR.joinpath(path), "rb") as f:
            content = f.read()
            CACHE[path] = content
            return content
    except Exception as e:
        log.error("can't get static file: %s" % e)


def get_mimetype(path) -> str | None:
    mimetype, _ = mimetypes.guess_type(STATIC_DIR.joinpath(path))
    return mimetype


class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Basic Web Server"
    protocol_version = "HTTP/1.1"

    def __init__(self, *args, **kwargs) -> None:
        self.paths = {
            "/": "index.html",
            "/about": "pages/about.html",
            "/favicon.ico": "images/favicon.ico",
            "/main.js": "scripts/main.js",
            "/style.css": "css/style.css",
        }
        super().__init__(*args, **kwargs)

    def routing(self, path: str) -> Optional[Callable]:
        match path:
            case "/time":
                return self.handle_get_time
            case _:
                return lambda: self.handle_file(compress=True)

    def do_OPTIONS(self):
        self.handle_request()

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def handle_request(self):
        log.debug("%s %s" % (self.command, self.path))
        if self.command == "GET":
            (self.routing(self.path) or self.handle_not_found)()
        else:
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)
        self.close_connection = True

    def handle_not_found(self):
        self.send_error(HTTPStatus.NOT_FOUND)

    def send_error(self, code, message=None):
        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def handle_file(self, compress=True):
        filepath = self.paths.get(self.path)
        if not filepath:
            log.debug("filepath for %r not found" % self.path)
            self.handle_not_found()
            return
        log.debug("handling file %r by path %r" % (filepath, self.path))

        file = CACHE.get(filepath, get_static_file(filepath))
        if not file:
            self.handle_not_found()
            return
        self.send_response(HTTPStatus.OK)
        if mimetype := get_mimetype(filepath):
            self.send_header("Content-Type", mimetype)
        if compress:
            file = gzip.compress(file)
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(file)))
        self.end_headers()
        self.wfile.write(file)

    def handle_get_time(self):
        time_resp = json.dumps({"time": time.strftime("%H:%M:%S")}).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", f"{len(time_resp)}")
        self.end_headers()
        self.wfile.write(time_resp)


def parse_args():
    parser = argparse.ArgumentParser()

    def validate_port(arg: str) -> int:
        try:
            if (port := int(arg)) and port <= 0:
                raise
        except:
            raise argparse.ArgumentTypeError("invalid port, should be positive number")
        else:
            return port

    parser.add_argument("-p", "--port", default=PORT, type=validate_port)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not STATIC_DIR.exists() or not STATIC_DIR.is_dir():
        exit(1)

    with socketserver.TCPServer(("", args.port), BasicRequestHandler) as httpd:
        shutdown = threading.Thread(target=httpd.shutdown, daemon=True)
        try:
            host, port = httpd.server_address
            print(f"start listening on {host}:{port}...")
            httpd.serve_forever()
        except:
            print("shutting down...")
            shutdown.start()
        finally:
            shutdown.join()
            sys.exit(0)
