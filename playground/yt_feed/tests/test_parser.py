import unittest

from parser import YTFeedParser
from .mocks import raw_test_feed, TEST_FEED


class ParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = YTFeedParser(raw_test_feed())

    def test_parser(self):
        self.assertListEqual(self.parser.entries, TEST_FEED.entries)
