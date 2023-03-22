import unittest

from pypika import Table

from person import Person, PersonStorage
from .db_hooks import DBHooks

DB_FILE = "test_person_storage.db"
CREATE_TABLE = """
    CREATE TABLE tb_persons (
        name VARCHAR  NOT NULL,
        age  SMALLINT NOT NULL CHECK (age > 0)
)"""


class PersonStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_hooks = DBHooks(DB_FILE)
        if not cls.db_hooks.init_db([CREATE_TABLE]):
            raise Exception("init db failed")

        cls.stor = PersonStorage(DB_FILE)
        cls.t = Table("tb_persons")
        cls.insert_persons = [Person("A", 1), Person("B", 2)]

    @classmethod
    def tearDownClass(cls):
        if not cls.db_hooks.drop_db():
            raise Exception("drop db failed")

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

    def test2_select_one(self):
        person, err = self.stor.select_one(self.t.rowid == 1)
        self.assertIs(err, None, f"unexpected error: {err}")
        self.assertIsInstance(person, Person, f"unexpected person type: {person}")
        self.assertEqual(person, self.insert_persons[0], f"should be equal")

    def test3_update1(self):
        count, err = self.stor.update(
            Person("C", 30),
            where=(self.t.name == "A"),
        )
        self.assertIsNone(err)
        self.assertEqual(count, 1)

    def test4_update2(self):
        new_person = Person("D", 40)
        count, err = self.stor.update(
            new_person, where=[self.t.name == "B", self.t.age == 2]
        )
        self.assertIsNone(err)
        self.assertEqual(count, 1)

    def test5_select_all(self):
        persons, err = self.stor.select()
        self.assertIsNone(err)
        self.assertEqual(persons, [Person("C", 30), Person("D", 40)])


if __name__ == "__main__":
    unittest.main()
