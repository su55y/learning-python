import unittest

from . import db_hooks
from storage import storage


class StorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not db_hooks.init_db():
            raise Exception("create database failed")
        cls.stor = storage.Storage("test.db")
        cls.tb_persons = "tb_persons"
        cls.insert_data = [("A", 1), ("B", 2)]
        cls.invalid_data = [("A", 0)]

    @classmethod
    def tearDownClass(cls):
        if not db_hooks.drop_table():
            raise Exception("drop table failed")
        if not db_hooks.drop_database():
            raise Exception("remove database failed")

    def test1_insert(self):
        count, err = self.stor.insert(self.tb_persons, self.insert_data)
        self.assertIsNone(err, f"unexpected err: {err}")
        self.assertEqual(count, len(self.insert_data), "unexpected rowcount")

    def test2_select(self):
        data, err = self.stor.select(self.tb_persons)
        self.assertIsNone(err, f"unexpected err: {err}")
        self.assertEqual(
            data,
            self.insert_data,
            f"unexpected select result: {data}",
        )

    def test3_invalid_insert(self):
        count, err = self.stor.insert(self.tb_persons, self.invalid_data)
        self.assertEqual(count, 0, "should be 0")
        self.assertIsInstance(err, Exception, f"unexpected error type: {repr(err)}")


if __name__ == "__main__":
    unittest.main()
