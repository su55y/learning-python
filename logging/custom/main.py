import logging
from custom_formatter import CustomFormatter

log: logging.Logger


def init_logger(**kwargs):
    global log
    log = logging.getLogger(kwargs.get("name", __name__))
    log.setLevel(kwargs.get("level", logging.WARNING))
    handler = logging.StreamHandler()
    formatter = CustomFormatter(datefmt=kwargs.get("datefmt", "%H:%M:%S %d/%m/%y"))
    handler.setFormatter(formatter)
    log.addHandler(handler)


def div(x, y):
    if not all(isinstance(arg, (int, float)) for arg in [x, y]):
        log.warning("x or y are not number, now something is going to happen")

    log.debug(f"try {x} / {y}")
    try:
        log.info(f"{x} / {y} = {x / y}")
    except TypeError as e:
        log.error(f"can't divide {x} by {y}: {e}")
    except ZeroDivisionError as e:
        log.critical(f"can't divide {x} by {y}: {e}")
        exit(1)


def main():
    div(1, 2)
    div(0, "\U0001F43C")
    div(1, 0)
    log.info("done")


if __name__ == "__main__":
    init_logger(level=logging.DEBUG)
    main()
