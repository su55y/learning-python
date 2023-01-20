import logging

logging.basicConfig(
  level=logging.INFO,
  # filename="log",
  # filemode="w",
  format="\x1b[38;5;44m%(asctime)s [%(levelname)s]:\x1b[0m %(message)s",
  datefmt="%H:%M:%S %d/%m/%y"
)

logging.debug("debug log")
logging.info("info log")
logging.warning("warning log")
logging.error("error log")
logging.critical("critical log")
