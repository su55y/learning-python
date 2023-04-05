from enum import Enum, auto
import logging


class HandlerType(Enum):
    Stream = auto()
    File = auto()


def create_logger(**kwargs):
    logger = logging.getLogger(kwargs.get("name", __name__))
    if level := kwargs.get("level"):
        logger.setLevel(level)

    match kwargs.get("handler_type", HandlerType.Stream):
        case HandlerType.Stream:
            handler = logging.StreamHandler()
        case HandlerType.File:
            path = kwargs.get("path")
            if not path:
                path = f"{__name__}.log"
            handler = logging.FileHandler(path)
        case _:
            raise NotImplemented(f"this handler type not implemented yet")

    if format := kwargs.get("format"):
        handler.setFormatter(logging.Formatter(format))

    logger.addHandler(handler)
    return logger
