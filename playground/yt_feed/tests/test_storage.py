from datetime import datetime
from pathlib import Path
import unittest

from storage import DBHooks, Storage
from .mocks import sample_channel, sample_entries


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
        self.assertEqual(self.stor.add_channels([sample_channel()]), 1)
        self.assertEqual(self.stor.add_entries(sample_channel()), len(sample_entries()))

    def test2_select(self):
        channel = self.stor.channel(sample_channel().channel_id, -1)
        self.assertIsNotNone(channel)
        channel.entries = sorted(
            channel.entries, key=lambda e: datetime.fromisoformat(e.updated)
        )
        self.assertEqual(channel, sample_channel())

    def test2_select_not_found(self):
        self.assertIsNone(self.stor.channel("-", -1))
        entries = self.stor.select_entries("-", -1)
        self.assertEqual(len(entries), 0)

    def test3_insert_duplicate(self):
        count = self.stor.add_entries(sample_channel())
        self.assertEqual(count, 0)
