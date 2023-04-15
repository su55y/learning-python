import argparse
from http import HTTPStatus
import http.server
import gzip
import os
import sys
import time
import threading

HOST = "localhost"
PORT = 8000
STATIC_DIR = os.path.join(os.getcwd(), "static")


def get_static_file(path):
    try:
        with open(os.path.join(STATIC_DIR, path), "rb") as f:
            return f.read()
    except Exception as e:
        print(e)


class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Basic Web Server"
    protocol_version = "HTTP/1.1"

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
            case _:
                return ""

    def routing(self):
        return {
            "/": self.handle_page,
            "/index.html": self.handle_page,
            "/about": self.handle_page,
            "/time": self.handle_get_time,
            "/favicon.ico": self.handle_icon,
        }

    def handle_icon(self):
        if image := get_static_file(self.filter_path(self.path)):
            compressed = gzip.compress(image)
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "image/x-icon")
            self.send_header("Content-Encoding", "gzip")
            self.send_header("Content-Length", f"{len(compressed)}")
            self.end_headers()
            self.wfile.write(compressed)
        else:
            self.handle_not_found()

    def handle_page(self):
        if page := get_static_file(self.filter_path(self.path)):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", f"{len(page)}")
            self.end_headers()
            self.wfile.write(page)
        else:
            self.handle_not_found()

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

    def handle_get_time(self):
        time_str = time.strftime("%H:%M:%S").encode()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", f"{len(time_str)}")
        self.end_headers()
        self.wfile.write(time_str)

    def handle_not_found(self):
        self.send_error(HTTPStatus.NOT_FOUND)

    def send_error(self, code, message=None):
        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def shutdown(self):
        self.server.socket.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--addr", default=HOST)
    parser.add_argument("-p", "--port", default=PORT)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    with http.server.HTTPServer((args.addr, args.port), BasicRequestHandler) as httpd:
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
