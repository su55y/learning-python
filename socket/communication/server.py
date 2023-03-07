import os
import socket
import signal
from contextlib import contextmanager
import os.path
from datetime import datetime

SOCKET_FILE = "/tmp/test.sock"


@contextmanager
def server_socket():
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        server_socket.bind(SOCKET_FILE)
        server_socket.listen(1)
        print("listening...")

        yield server_socket
    finally:
        server_socket.close()
        print("socket closed")
        os.remove(SOCKET_FILE)


def signal_handler(signum, frame):
    print("shutting down...")
    raise SystemExit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)

    with server_socket() as s:
        while True:
            client_socket, _ = s.accept()

            try:
                match cmd := client_socket.recv(4).decode():
                    case "file":
                        with open(os.path.abspath(__file__), "rb") as f:
                            client_socket.sendall(f.read())
                        print("file cmd handled")
                    case "time":
                        client_socket.sendall(
                            datetime.now().time().strftime("%H:%M:%S").encode()
                        )
                        print("time cmd handled")
                    case _:
                        print(f"unkwown cmd '{cmd}'")
            except Exception as e:
                print(e)
            finally:
                client_socket.close()


if __name__ == "__main__":
    main()
