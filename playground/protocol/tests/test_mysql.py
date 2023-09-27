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
        self.assertEqual(
            self.stor.insert(
                "insert into tb_test (id, foo) values (?, ?)", [(1, "bar")]
            ),
            1,
        )

    # def test2_select(self):
    #     self.assertEqual(self.stor.select(1), [("1", "bar")])
