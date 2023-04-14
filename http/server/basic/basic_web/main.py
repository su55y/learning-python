import http.server
import os
import signal
import sys
import time
import threading

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
            self.send_error(405)

    def filter_path(self, path):
        match path:
            case "/":
                return "index.html"
            case "/about":
                return "pages/about.html"
            case _:
                return ""

    def routing(self):
        return {
            "/": self.handle_page,
            "/index.html": self.handle_page,
            "/about": self.handle_page,
            "/time": self.handle_get_time,
        }

    def handle_page(self):
        if page := get_static_file(self.filter_path(self.path)):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
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
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(time.strftime("%H:%M:%S").encode())

    def handle_not_found(self):
        self.send_error(404)

    def send_error(self, code, message=None):
        self.send_response(code, message)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def shutdown(self):
        self.server.socket.close()


if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), BasicRequestHandler) as httpd:
        shutdown = threading.Thread(target=httpd.shutdown, daemon=True)
        try:
            httpd.serve_forever()
        except:
            print("shutting down...")
            shutdown.start()
        finally:
            shutdown.join()
            sys.exit(0)
