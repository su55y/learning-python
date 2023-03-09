from datetime import datetime
import sys
import threading
import time
import queue


def ticker(q: queue.Queue):
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        sys.stdout.write(f"tick {timestamp}")
        sys.stdout.flush()
        sys.stdout.write("\033[2K\033[1E")
        if q.qsize() and q.get_nowait():
            sys.stdout.write(f"{timestamp} tack\n")
        else:
            time.sleep(1)


def main():
    q = queue.Queue()
    ticker_thread = threading.Thread(target=ticker, daemon=True, args=(q,))
    ticker_thread.start()
    try:
        while True:
            if input() == "":
                q.put(1)
    except KeyboardInterrupt:
        exit(0)


if __name__ == "__main__":
    main()
