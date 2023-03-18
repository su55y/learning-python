from contextlib import contextmanager
import math
import sqlite3
import unittest

from db.hooks import DBHooks
from db.queries import *
from models import City


class BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_hooks = DBHooks(db_file="countries.db")
        if not cls.db_hooks.init_db(
            [
                TB_COUNTRIES_SQL,
                TB_CAPITALS_SQL,
                AFTER_COUNTRY_INSERT,
                COUNTIES_INSERT_SQL,
            ]
        ):
            raise Exception("init db failed")

        @contextmanager
        def get_cursor():
            conn = sqlite3.connect(cls.db_hooks.db_file)
            try:
                yield conn.cursor()
            except Exception as e:
                raise e
            finally:
                conn.commit()
                conn.close()

        cls.get_cur = lambda _: get_cursor()

    @classmethod
    def tearDownClass(cls):
        if not cls.db_hooks.drop_db():
            raise Exception("drop db failed")

    def test1_select(self):
        rows = None
        with self.get_cur() as cur:
            cur.execute("SELECT name FROM countries")
            rows = cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertEqual(len(rows), 2, "unexpected rowcount")
        countries = list(*zip(*rows))
        self.assertEqual(countries, ["Peru", "UK"])

    def test1_select_all(self):
        rows = None
        with self.get_cur() as cur:
            cur.execute(
                """SELECT countries.name, capitals.name
                   FROM countries, capitals
                   WHERE countries.capital = capitals.name"""
            )
            rows = cur.fetchall()
        self.assertIsNotNone(rows)
        self.assertEqual(len(rows), 2, "unexpected rowcount")
        self.assertEqual(rows, [("Peru", "Lima"), ("UK", "London")])

    def test2_insert(self):
        count = None
        new_countries = [("Senegal", "Dakar"), ("France", "Paris")]
        with self.get_cur() as cur:
            count = cur.executemany(
                "INSERT INTO countries VALUES (?, ?)", new_countries
            ).rowcount
        self.assertEqual(len(new_countries), count, "unexpected rowcount")

    def test3_update(self):
        count = None
        new_capitals = [
            (14.720654216814015, -17.467541613688535, "Dakar"),
            (48.8597371418384, 2.3504661150379915, "Paris"),
            (-12.042084062782227, -77.04339743742001, "Lima"),
            (51.512072184983296, -0.13596405470562567, "London"),
        ]
        with self.get_cur() as cur:
            count = cur.executemany(
                "UPDATE capitals SET lat = ?, lon = ? WHERE name = ?", new_capitals
            ).rowcount
        self.assertEqual(count, len(new_capitals), "unexpected rowcount")

    def test4_utils(self):
        paris = dakar = None
        query = "SELECT * FROM capitals WHERE name = '%s'"
        with self.get_cur() as cur:
            dakar_row = cur.execute(query % "Dakar").fetchone()
            paris_row = cur.execute(query % "Paris").fetchone()
        dakar = City(*dakar_row)
        paris = City(*paris_row)
        distance = dakar.distance_to(paris)
        self.assertTrue(math.isclose(distance, 4200, abs_tol=10), "should be 4200±10")
