from pathlib import Path
import unittest

from storage import DBHooks, Storage
from .mocks import TEST_FEED, TEST_ENTRIES


class StorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_file = Path("/tmp/test.db")
        if cls.db_file.exists():
            cls.db_file.unlink()
        cls.db_hooks = DBHooks(cls.db_file)
        if err := cls.db_hooks.init_db():
            raise err
        cls.stor = Storage(cls.db_file)

    @classmethod
    def tearDownClass(cls):
        if err := cls.db_hooks.drop_db():
            raise err

    def test1_insert(self):
        self.assertEqual(self.stor.add_feed(TEST_FEED), 1)
        self.assertEqual(self.stor.add_entries(TEST_FEED), len(TEST_ENTRIES))

    def test2_select(self):
        feed = self.stor.fetch_feed(TEST_FEED.channel_id)
        self.assertIsNotNone(feed)
        self.assertEqual(feed, TEST_FEED)

    def test2_select_entries(self):
        entries = self.stor.fetch_feed_entries(TEST_FEED.channel_id)
        self.assertEqual(entries, TEST_ENTRIES)
