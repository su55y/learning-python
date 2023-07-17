import argparse
import datetime as dt
import logging
import json
from pathlib import Path
import queue
import re
import socket
import time
import threading
from typing import Dict, Optional
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


def read_data(conn: socket.socket, limit: int = 1024 * 10) -> bytes:
    global log
    received_data = b""
    try:
        while len(received_data) < limit:
            chunk = conn.recv(1024)
            received_data += chunk
            if len(chunk) < 1024:
                break
        else:
            log.error("data size limit exceeded")
            return b'{"error":"data size limit exceeded"}'
    except Exception as e:
        log.error(e)
        return b'{"error":"error while reading data"}'
    else:
        return received_data


def handle_command(request_data: Dict) -> Dict:
    global download_queue
    match command := request_data.get("command"):
        case "queue":
            return {"queue_size": download_queue.qsize()}
        case "append":
            if url := request_data.get("url"):
                if not re.match(r"^https.+$", url):
                    return {"error": "invalid url"}
                else:
                    download_queue.put(url)
                    return {"queue_size": download_queue.qsize()}
            else:
                return {"error": "url should be present for append command"}
        case _:
            return {"error": "unkown command %r" % command}


def handle_request(conn: socket.socket) -> Dict:
    global log
    raw_data = read_data(conn)
    try:
        request_data = json.loads(raw_data)
        if request_data.get("error"):
            return request_data
        if request_data.get("command"):
            return handle_command(request_data)
    except json.JSONDecodeError as e:
        log.error("decode error: %s" % e)
        return {"error": "invalid json"}
    except Exception as e:
        log.error("decode data error: %s" % e)
    return {"error": "invalid request"}


def handle_connection(conn: socket.socket):
    global log
    try:
        resp = handle_request(conn)
        conn.sendall(json.dumps(resp).encode())
    except Exception as e:
        log.error(e)
    finally:
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
            if download_queue.empty():
                time.sleep(1)
            else:
                url = download_queue.get()
                download_thread = threading.Thread(
                    target=download_file, args=(url, args.download_dir)
                )
                download_thread.start()
                download_thread.join()
    except KeyboardInterrupt:
        if size := download_queue.qsize():
            log.info("%d jobs in queue" % size)
    except Exception as e:
        log.error(e)

    log.info("shutting down...")
    shutdown_event.set()
    server_thread.join()
