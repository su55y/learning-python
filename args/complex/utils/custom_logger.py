import logging


class CustomLogger(logging.Logger):
    pass

    def __init__(self, name: str, level) -> None:
        super().__init__(name, level)
        self.setFormatter()

    def setFormatter(self):
        ch = logging.StreamHandler()
        ch.setLevel(self.level)
        ch.setFormatter(CustomFormatter())
        self.addHandler(ch)


class CustomFormatter(logging.Formatter):
    pink_bold = "\x1b[38;5;204;1m"
    pink_underline_bold = "\x1b[38;5;204;4;1m"
    white_bold = "\x1b[1m"
    white_bold_italic = "\x1b[1;3m"
    yellow_bold = "\x1b[38;5;11;1m"
    yellow_bold_italic = "\x1b[38;5;11;1;3m"
    red_bold = "\x1b[31;1m"
    red_bg_bold = "\x1b[48;5;88;1m"
    reset = "\x1b[0m"
    prefix = "%(asctime)s [%(levelname)s]: "
    message_file = "%(message)s (%(filename)s:%(lineno)d)"
    message_file_func = "%(message)s (%(filename)s:%(funcName)s:%(lineno)d)"
    debug_msg_fmt = (
        f"%(message)s{reset} \x1b[38;5;197;1;3m(%(filename)s:%(funcName)s:%(lineno)d)"
    )

    # docs.python.org/3/library/logging.html#logrecord-attributes
    FORMATS = {
        logging.DEBUG: f"{pink_bold}{prefix}{reset}{pink_underline_bold}{debug_msg_fmt}{reset}",
        logging.INFO: f"{white_bold}{prefix}{white_bold_italic}%(message)s{reset}",
        logging.WARNING: f"{yellow_bold}{prefix}{yellow_bold_italic}{message_file}{reset}",
        logging.ERROR: f"{red_bold}{prefix}{message_file_func}{reset}",
        logging.CRITICAL: f"{red_bg_bold}{prefix}%(message)s (%(filename)s:%(funcName)s:%(lineno)d){reset}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S %d/%m/%y")
        return formatter.format(record)
