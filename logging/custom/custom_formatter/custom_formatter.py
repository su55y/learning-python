import logging

from .formats import DEBUG_FMT, INFO_FMT, WARNING_FMT, ERROR_FMT, CRITICAL_FMT


class CustomFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._default = logging.Formatter(logging.BASIC_FORMAT)
        self.formatters = {
            logging.DEBUG: logging.Formatter(DEBUG_FMT, self.datefmt),
            logging.INFO: logging.Formatter(INFO_FMT, self.datefmt),
            logging.WARNING: logging.Formatter(WARNING_FMT, self.datefmt),
            logging.ERROR: logging.Formatter(ERROR_FMT, self.datefmt),
            logging.CRITICAL: logging.Formatter(CRITICAL_FMT, self.datefmt),
        }

    def format(self, record):
        return self.formatters.get(record.levelno, self._default).format(record)
