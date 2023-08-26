import http.server
import sys
import time
import threading

PORT = 8000


class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Basic Server"

    def do_GET(self):
        (self.handle_hello_world if self.path == "/" else self.handle_not_found)()

    def send_error(self, code: int, message=None, *_):
        self.send_response(code, message)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def handle_hello_world(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello World at %s" % time.strftime("%H:%M:%S").encode())

    def handle_not_found(self):
        self.send_error(404)


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
