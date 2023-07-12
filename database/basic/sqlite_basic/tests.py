import math
import sqlite3
import unittest

from db import init_db
from models import City


class BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        if err := init_db(cls.conn):
            raise err
        cls.cur = cls.conn.cursor()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test1_select(self):
        rows = self.cur.execute("SELECT name FROM countries").fetchall()
        self.assertEqual(rows, [("Peru",), ("UK",)])

    def test1_select_all(self):
        rows = self.cur.execute(
            """SELECT countries.name, capitals.name
               FROM countries, capitals
               WHERE countries.capital = capitals.name"""
        ).fetchall()
        self.assertEqual(rows, [("Peru", "Lima"), ("UK", "London")])

    def test2_insert(self):
        new_countries = [("Senegal", "Dakar"), ("France", "Paris")]
        count = self.cur.executemany(
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
        count = self.cur.executemany(
            "UPDATE capitals SET lat = ?, lon = ? WHERE name = ?", new_capitals
        ).rowcount
        self.assertEqual(count, len(new_capitals), "unexpected rowcount")

    def test4_city_distance(self):
        query = "SELECT * FROM capitals WHERE name = '%s'"
        paris = City(*self.cur.execute(query % "Paris").fetchone())
        dakar = City(*self.cur.execute(query % "Dakar").fetchone())
        self.assertTrue(math.isclose(paris.distance_to(dakar), 4200, abs_tol=10))
