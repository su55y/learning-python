import unittest

from .db_hooks import DBHooks
from storage import storage

DB_FILE = "test_storage.db"
CREATE_TABLE = """
    CREATE TABLE tb_persons (
        name VARCHAR  NOT NULL,
        age  SMALLINT NOT NULL CHECK (age > 0)
)"""


class StorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_hooks = DBHooks(DB_FILE)
        if not cls.db_hooks.init_db([CREATE_TABLE]):
            raise Exception("init db failed")
        cls.stor = storage.Storage(DB_FILE)
        cls.tb_persons = "tb_persons"
        cls.insert_data = [("A", 1), ("B", 2)]
        cls.invalid_data = [("A", 0)]

    @classmethod
    def tearDownClass(cls):
        if not cls.db_hooks.drop_db():
            raise Exception("drop db failed")

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
