import unittest

from ..storage import Storage
from ..storage.db import SQLite


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stor = Storage(SQLite(":memory:"))
