from pathlib import Path
import secrets
import sqlite3
import unittest

from storage.db import SQLite
from storage import Storage


def init_db(file: Path):
    with sqlite3.connect(file) as conn:
        cur = conn.cursor()
        cur.execute("create table tb_test(id number primary key, foo text(255))")
        conn.commit()


class TestMySQL(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = Path("/tmp/storage%s.db" % secrets.token_hex(8))
        if cls.file.exists():
            cls.file.unlink()
        init_db(cls.file)
        cls.stor = Storage(SQLite(str(cls.file)))

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.file.exists():
            cls.file.unlink()

    def test1_insert(self):
        count = self.stor.insert(
            "insert into tb_test (id, foo) values (?, ?)", [(1, "bar")]
        )
        self.assertEqual(count, 1)

    def test2_select(self):
        rows = self.stor.select("select * from tb_test")
        self.assertEqual(rows, [(1, "bar")])

    def test3_delete(self):
        count = self.stor.delete("delete from tb_test where id=1")
        self.assertEqual(count, 1)
