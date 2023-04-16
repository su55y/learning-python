import argparse
from http import HTTPStatus
import http.server
import json
import gzip
import mimetypes
import os
import socketserver
import sys
import time
import threading

PORT = 8000
STATIC_DIR = os.path.join(os.getcwd(), "static")
CACHE = dict()


def get_static_file(path) -> bytes | None:
    try:
        filepath = os.path.join(STATIC_DIR, path)
        with open(filepath, "rb") as f:
            content = f.read()
            CACHE[path] = content
            return content
    except Exception as e:
        print(e)


def get_mimetype(path) -> str | None:
    mimetype, _ = mimetypes.guess_type(os.path.join(STATIC_DIR, path))
    return mimetype


class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Basic Web Server"
    protocol_version = "HTTP/1.1"

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
        if self.command == "GET":
            self.routing().get(self.path, self.handle_not_found)()
        else:
            self.send_error(HTTPStatus.METHOD_NOT_ALLOWED)

    def filter_path(self, path):
        match path:
            case "/":
                return "index.html"
            case "/about":
                return "pages/about.html"
            case "/favicon.ico":
                return "images/favicon.ico"
            case "/main.js":
                return "scripts/main.js"
            case "/style.css":
                return "css/style.css"
            case _:
                return ""

    def routing(self):
        return {
            "/": self.handle_file,
            "/index.html": self.handle_file,
            "/about": self.handle_file,
            "/time": self.handle_get_time,
            "/favicon.ico": self.handle_file,
            "/style.css": self.handle_file,
            "/main.js": lambda: self.handle_file(compress=False),
        }

    def handle_not_found(self):
        self.send_error(HTTPStatus.NOT_FOUND)

    def send_error(self, code, message=None):
        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def handle_file(self, compress=True):
        filepath = self.filter_path(self.path)
        if file := CACHE.get(filepath, get_static_file(filepath)):
            self.send_response(HTTPStatus.OK)
            if mimetype := get_mimetype(filepath):
                self.send_header("Content-Type", mimetype)
            if compress:
                file = gzip.compress(file)
                self.send_header("Content-Encoding", "gzip")
                self.send_header("Content-Length", f"{len(file)}")
            else:
                self.send_header("Content-Length", f"{len(file)}")
            self.end_headers()
            self.wfile.write(file)
        else:
            self.handle_not_found()

    def handle_get_time(self):
        time_resp = json.dumps({"time": time.strftime("%H:%M:%S")}).encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", f"{len(time_resp)}")
        self.end_headers()
        self.wfile.write(time_resp)

    def shutdown(self):
        self.server.socket.close()


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
