import socket
import queue
import threading
import re
import logging
import os.path
import urllib.request

import config

download_queue = queue.Queue()
shutdown_event = threading.Event()
log: logging.Logger


def init_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(config.LOG_FMT))
    log.addHandler(sh)


def handle_connection(conn):
    resp = ""
    data = conn.recv(1024).decode().strip()
    log.info(f"received data: {data}")
    match data:
        case "stop":
            resp = "stop cmd".encode()
            shutdown_event.set()
        case _:
            if re.match(r"^https.+$", data):
                download_queue.put(data)
                resp = "URL added to queue".encode()

    conn.sendall(resp)
    conn.close()


def download_file(url):
    filename = os.path.join(config.DOWNLOAD_DIR, url.split("/")[-1])
    try:
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        log.error(e)


def listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server_address = (config.HOST, config.PORT)
        server.bind(server_address)
        server.settimeout(config.TIMEOUT)
        server.listen(1)
        log.info(f"listening on {server_address}")

        while not shutdown_event.is_set():
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue

            log.info(f"received connection from {addr}")
            t = threading.Thread(target=handle_connection, args=(conn,))
            t.start()


def main():
    server_thread = threading.Thread(target=listener)
    server_thread.start()
    try:
        while not shutdown_event.is_set():
            if not download_queue.empty():
                url = download_queue.get()
                download_thread = threading.Thread(target=download_file, args=(url,))
                download_thread.start()
                download_thread.join()
    except KeyboardInterrupt:
        log.info("shutting down...")
    except Exception as e:
        log.info(e)

    shutdown_event.set()
    server_thread.join()


if __name__ == "__main__":
    init_logger()
    main()
