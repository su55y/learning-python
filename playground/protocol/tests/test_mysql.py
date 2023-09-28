import unittest

from storage.db import MySQL
from storage import Storage

MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": "3306",
    "user": "root",
    "password": "",
    "database": "db_protocol",
}


class TestMySQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stor = Storage(MySQL(**MYSQL_CONFIG))

    def test1_insert(self):
        count = self.stor.insert(
            "insert into tb_test (id, foo) values (%s, %s)",
            [(1, "bar")],
        )
        self.assertEqual(count, 1)

    def test2_select(self):
        rows = self.stor.select("select * from tb_test where id=1")
        self.assertEqual(rows, [(1, "bar")])

    def test3_delete(self):
        count = self.stor.delete("delete from tb_test where id=1")
        self.assertEqual(count, 1)
