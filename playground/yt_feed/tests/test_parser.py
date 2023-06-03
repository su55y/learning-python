import unittest

from parser import YTFeedParser
from .mocks import raw_test_feed, TEST_FEED, TEST_ENTRIES


class ParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = YTFeedParser(raw_test_feed())

    def test_parser(self):
        self.assertEqual(self.parser.title, TEST_FEED.title)
        self.assertEqual(self.parser.entries, TEST_ENTRIES)
