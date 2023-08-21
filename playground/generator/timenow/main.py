import datetime as dt
import time


def time_generator():
    while True:
        yield dt.datetime.now().strftime("%T")


if __name__ == "__main__":
    timenow = time_generator()
    for _ in range(5):
        print(next(timenow))
        time.sleep(1)
