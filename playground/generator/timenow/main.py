import time


def time_generator():
    while True:
        yield time.strftime("%T")


if __name__ == "__main__":
    timenow_gen = time_generator()
    for timenow in timenow_gen:
        print(timenow)
        time.sleep(1)
