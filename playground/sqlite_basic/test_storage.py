import unittest

from . import db_hooks
from storage import storage


class StorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not db_hooks.init_db():
            raise Exception("create database failed")
        cls.stor = storage.Storage("test.db")
        cls.insert_data = [
            {"name": "A", "age": 1},
            {"name": "B", "age": 2},
        ]

    @classmethod
    def tearDownClass(cls):
        if not db_hooks.drop_table():
            raise Exception("drop table failed")
        if not db_hooks.drop_database():
            raise Exception("remove database failed")

    def test1_insert(self):
        count = self.stor.insert(self.insert_data)
        self.assertEqual(count, len(self.insert_data), "unexpected rowcount")

    def test2_select(self):
        data = self.stor.select()
        self.assertEqual(
            data,
            [(person["name"], person["age"]) for person in self.insert_data],
            f"unexpected select result: {data}",
        )


if __name__ == "__main__":
    unittest.main()
