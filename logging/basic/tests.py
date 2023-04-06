from datetime import datetime
import io
import logging
from os import remove, path
import unittest

from basic_logger import HandlerType, create_logger


SIMPLE_LOG_FMT = "%(levelname)s %(message)s"
RICH_LOG_FMT = "[%(asctime)-.19s %(levelname)-.4s] %(message)s (%(filename)s)"


class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stream = io.StringIO()
        cls.rich_logger = create_logger(
            name="rich_logger",
            format=RICH_LOG_FMT,
            handler=logging.StreamHandler(cls.stream),
            level=logging.INFO,
        )
        cls.filename = "test.log"
        cls.file_logger = create_logger(
            name="file_logger",
            filename=cls.filename,
            format=SIMPLE_LOG_FMT,
            handler_type=HandlerType.File,
        )

    @classmethod
    def tearDownClass(cls):
        if not cls.stream.closed:
            cls.stream.close()
        if path.exists(cls.filename) and path.isfile(cls.filename):
            remove(cls.filename)

    def test_file_log(self):
        self.file_logger.warning("file log")
        with open(self.filename) as file:
            record = file.readline()
        self.assertEqual(record, "WARNING file log\n")

    def test_log_fmt(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp} INFO] rich fmt log ({path.basename(__file__)})\n"
        self.rich_logger.info(f"rich fmt log")
        self.assertEqual(self.stream.getvalue(), log_msg)
