import http.server
import signal
import socketserver
import sys
import time
import threading

PORT = 8000


class BasicRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Basic Server"

    def handle_get_time(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(time.strftime("%H:%M:%S").encode())

    def handle_not_found(self):
        self.send_error(404)

    def routing(self):
        return {
            "/time": self.handle_get_time,
        }

    def do_GET(self):
        self.routing().get(self.path, self.handle_not_found)()

    def send_error(self, code, message=None, explain=None):
        self.send_response(code, message)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def shutdown(self):
        self.server.socket.close()


def raiser():
    raise


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *_: raiser())
    with socketserver.TCPServer(("", PORT), BasicRequestHandler) as httpd:
        shutdown = threading.Thread(target=httpd.shutdown, daemon=True)
        try:
            httpd.serve_forever()
        except:
            print("shutting down...")
            shutdown.start()
        finally:
            shutdown.join()
            sys.exit(0)
