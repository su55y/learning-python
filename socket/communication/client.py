import socket
from typing import Tuple

SOCKET_FILE = "/tmp/test.sock"


def send_cmd(cmd: str, length=1024) -> Tuple[bytes, Exception | None]:

    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
            s.connect(SOCKET_FILE)
            s.sendall(cmd.encode())
            return s.recv(length), None
    except Exception as e:
        return b"", e


def main():
    time, err = send_cmd("time")
    if not err:
        print(f"time: {time.decode()}")
    else:
        print(err)

    server_copy = "server_copy.py"
    file, err = send_cmd("file", 2048)
    if not err:
        try:
            with open(server_copy, "wb") as f:
                length = f.write(file)
                print(f"{length} bytes written to {server_copy}")
        except Exception as e:
            print(f"can't write {server_copy}: {e}")
    else:
        print(err)


if __name__ == "__main__":
    main()
