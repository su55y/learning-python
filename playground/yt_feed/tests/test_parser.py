import unittest

from parser import YTFeedParser
from .mocks import raw_test_feed, TEST_FEED


class ParserTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = YTFeedParser(raw_test_feed())

    def test_parser(self):
        feed = self.parser.parse_feed()
        self.assertEqual(feed.title, TEST_FEED.title)
        self.assertEqual(feed.channel_id, TEST_FEED.channel_id)
        self.assertListEqual(feed.entries, TEST_FEED.entries)
