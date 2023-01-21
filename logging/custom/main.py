from sys import exit
from utils.custom_logger import CustomLogger

log = CustomLogger(__name__, 0)


def div(x, y):
    if not all(isinstance(arg, (int, float)) for arg in [x, y]):
        log.warning("x or y are not number, now something is going to happen")

    log.debug(f"try {x} / {y}")
    try:
        print(f"{x} / {y} = {x / y}")
    except TypeError as e:
        log.error(f"can't divide {x} by {y}: {e}")
    except ZeroDivisionError as e:
        log.critical(f"can't divide {x} by {y}: {e}")
        exit(1)


def main():
    div(0, "\U0001F43C")
    div(1, 0)
    log.info("done")
    exit(0)


if __name__ == "__main__":
    main()
