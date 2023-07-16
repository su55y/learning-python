import argparse
import datetime as dt
import logging
from pathlib import Path
import queue
import re
import socket
import threading
import urllib.request


download_queue = queue.Queue()
shutdown_event = threading.Event()
log: logging.Logger


def init_logger():
    global log
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)",
            datefmt="%H:%M:%S %d/%m/%y",
        )
    )
    log.addHandler(sh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(conflict_handler="resolve")
    parser.add_argument(
        "-d",
        "--download-dir",
        default=Path(__file__).resolve().parent.joinpath("downloads"),
        type=Path,
        metavar="PATH",
        help="download directory (default: %(default)s)",
    )
    parser.add_argument(
        "-h",
        "--host",
        default="localhost",
        help="host (default: %(default)s)",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="port (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5,
        metavar="INT",
        help="timeout seconds (default: %(default)s)",
    )
    return parser.parse_args()


def handle_connection(conn):
    global log, download_queue, shutdown_event
    data = conn.recv(1024).decode().strip()
    log.info(f"received data: {data!r}")
    match data:
        case "stop":
            log.info("shutting down...")
            shutdown_event.set()
        case "queue":
            conn.sendall(b"%d" % download_queue.qsize())
        case _:
            if re.match(r"^https.+$", data):
                download_queue.put(data)
                conn.sendall(b"%d" % download_queue.qsize())
    conn.close()


def download_file(url: str, dir: Path):
    global log
    filename = url.split("/").pop() or "unnamed%d" % (dt.datetime.now().microsecond)
    filepath = dir.joinpath(filename)
    log.info("download from %s to %s" % (url, filepath))
    try:
        urllib.request.urlretrieve(url, filepath)
    except Exception as e:
        log.error(e)


def listener(host: str, port: int, timeout: int):
    global shutdown_event
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.settimeout(timeout)
        server.listen(1)
        log.info("listening on %s:%d..." % (host, port))

        while not shutdown_event.is_set():
            try:
                conn, addr = server.accept()
            except socket.timeout:
                continue

            log.info(f"received connection from {addr}")
            t = threading.Thread(target=handle_connection, args=(conn,))
            t.start()


if __name__ == "__main__":
    args = parse_args()
    if not args.download_dir.exists():
        args.download_dir.mkdir()

    init_logger()

    server_thread = threading.Thread(
        target=listener, args=(args.host, args.port, args.timeout)
    )
    server_thread.start()
    try:
        while not shutdown_event.is_set():
            if not download_queue.empty():
                url = download_queue.get()
                download_thread = threading.Thread(
                    target=download_file, args=(url, args.download_dir)
                )
                download_thread.start()
                download_thread.join()
    except KeyboardInterrupt:
        log.info("shutting down...")
        if not download_queue.empty():
            log.info("%d jobs in queue" % download_queue.qsize())
    except Exception as e:
        log.error(e)

    shutdown_event.set()
    server_thread.join()
