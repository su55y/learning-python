import sys
import threading
import time
import queue


def ticker(q: queue.Queue):
    while True:
        time_now = time.strftime("%T")
        if q.qsize() and q.get_nowait():
            text = f"\r{time_now} tack\n"
        else:
            text = f"\rtick {time_now}"
        sys.stdout.write(text)
        sys.stdout.flush()
        time.sleep(1)


def main():
    q = queue.Queue()
    ticker_thread = threading.Thread(target=ticker, daemon=True, args=(q,))
    ticker_thread.start()
    while True:
        try:
            if input() == "":
                q.put(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
