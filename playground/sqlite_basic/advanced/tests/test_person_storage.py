import unittest

from pypika import Table

from . import db_hooks
from person import Person, PersonStorage


class PersonStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_file = "person.db"
        if not db_hooks.init_db(cls.db_file):
            raise Exception("create database failed")
        cls.stor = PersonStorage(cls.db_file)
        cls.t = Table("tb_persons")
        cls.insert_persons = [Person("A", 1), Person("B", 2)]

    @classmethod
    def tearDownClass(cls):
        if not db_hooks.drop_table(cls.db_file):
            raise Exception("drop table failed")
        if not db_hooks.drop_database(cls.db_file):
            raise Exception("remove database failed")

    def test1_insert(self):
        count, err = self.stor.insert(self.insert_persons)
        self.assertIs(err, None, f"insert error: {err}")
        self.assertEqual(count, len(self.insert_persons), "unexpected rowcount")

    def test2_select(self):
        persons, err = self.stor.select()
        self.assertIs(err, None, f"unexpected error: {err}")
        self.assertEqual(
            persons, self.insert_persons, f"unexpected select result: {persons}"
        )

    def test3_select_one(self):
        person, err = self.stor.select_one(self.t.rowid == 1)
        self.assertIs(err, None, f"unexpected error: {err}")
        self.assertIsInstance(person, Person, f"unexpected person type: {person}")
        self.assertEqual(person, self.insert_persons[0], f"should be equal")


if __name__ == "__main__":
    unittest.main()
