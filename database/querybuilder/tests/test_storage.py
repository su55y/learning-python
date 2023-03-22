import unittest

from pypika import Table

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
        cls.tb_persons = Table("tb_persons")
        cls.insert_data = [("A", 1), ("B", 2)]
        cls.update_data = ("C", 3)
        cls.invalid_data = ("A", 0)

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
        count, err = self.stor.insert(self.tb_persons, [self.invalid_data])
        self.assertEqual(count, 0, "should be 0")
        self.assertIsInstance(
            err, Exception, f"unexpected error type: {type(err).__name__}"
        )

    def test3_update(self):
        name, age = self.update_data
        count, err = self.stor.update(
            self.tb_persons,
            vals=[(self.tb_persons.name, name), (self.tb_persons.age, age)],
            where=(self.tb_persons.rowid == 1),
        )
        self.assertIsNone(err)
        self.assertEqual(count, 1)

    def test4_delete(self):
        name, _ = self.update_data
        count, err = self.stor.delete(
            self.tb_persons,
            where=(self.tb_persons.name == name),
        )
        self.assertIsNone(err)
        self.assertEqual(count, 1)


if __name__ == "__main__":
    unittest.main()
