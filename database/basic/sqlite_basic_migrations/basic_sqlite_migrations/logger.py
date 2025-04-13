import logging


def init_logger() -> None:
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s%(msecs)03d [\033[1;33m%(levelname)s\033[0m] %(message)s \033[1;33m%(filename)s:%(lineno)d\033[0m",
            datefmt="%S",
        )
    )
    log.addHandler(handler)
