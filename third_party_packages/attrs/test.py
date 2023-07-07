import sqlite3
import unittest
import uuid

from models import User


class TestUser(unittest.TestCase):
    def test_validation(self):
        self.assertRaises(ValueError, User, name="John", id="")
        self.assertRaises(ValueError, User, name="John", id=uuid.uuid4().bytes[:15])

    def test_conversion(self):
        user = User("John", id=uuid.uuid4())
        with sqlite3.connect(":memory:") as conn:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE user(uuid BLOB(16) PRIMARY KEY, name TEXT NOT NULL, rating TEXT DEFAULT '0')"
            )
            cur.execute(
                "INSERT INTO user (uuid, name) VALUES (?, ?)", (user.id.bytes, "John")
            )
            user2 = User(*cur.execute("SELECT name, uuid, rating FROM user").fetchone())

        self.assertEqual(user, user2)
