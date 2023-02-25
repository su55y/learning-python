from typing import List
import unittest

from country.country import CountriesStorage, Country
from . import init_db


class CountriesStorageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not init_db.create():
            raise Exception("create database failed")
        cls.stor = CountriesStorage(tb_countries="tb_countries")
        cls.t = cls.stor.tb_countries

    @classmethod
    def tearDownClass(cls):
        if not init_db.drop():
            raise Exception("drop database failed")

    def test1_insert(self):
        countries = [
            Country(None, "Ukraine", "Kyiv"),
            Country(None, "Poland", "Warsaw"),
            Country(None, "United Kingdom", "London"),
        ]
        count, insert_err = self.stor.insert(countries)
        self.assertIs(insert_err, None), f"insert error: {repr(insert_err)}"
        self.assertEqual(count, len(countries)), f"inserted rows count != 3 ({count})"

    def test2_select_one(self):
        ukraine, err = self.stor.select_one(where=(self.t.capital == "Kyiv"))
        self.assertIs(err, None), f"select error: {repr(err)}"
        self.assertIsInstance(
            ukraine, Country
        ), f"ukraine should be instance of Country ({ukraine}, {type(ukraine).__name__})"
        self.assertEqual(
            ukraine.country, "Ukraine"
        ), "country attribute should be 'Ukraine'"
        self.assertEqual(ukraine.capital, "Kyiv"), "capital attribute should be 'Kyiv'"

    def test3_select_one_not_found(self):
        raj, err = self.stor.select_one(where=(self.t.capital == "Dehli"))
        self.assertIs(err, None), f"select error: {repr(err)}"
        self.assertIs(raj, None), "raj should be None"

    def test4_select_all(self):
        countries, err = self.stor.select()
        self.assertIs(err, None), f"select error: {repr(err)}"
        self.assertIsInstance(
            countries, List
        ), f"countries should be list ({type(countries).__name__})"
        self.assertEqual(
            len(countries), 3
        ), f"countries length != 3 (len: {len(countries)})"
        self.assertIsInstance(
            countries[0], Country
        ), f"countries item should be instance of Country ({type(countries[0]).__name__})"

    def test5_select_where(self):
        countries, err = self.stor.select(where=(self.t.capital != "Kyiv"), limit=1)
        self.assertIs(err, None), f"select error: {repr(err)}"
        self.assertEqual(
            len(countries), 1
        ), f"countries length != 1 (len: {len(countries)})"
        self.assertTrue(
            Country(None, "Poland", "Warsaw") in countries
            or Country(None, "United Kingdom", "London") in countries
        ), f"Poland or UK should be in countries: {countries}"

    def test6_insert_one(self):
        count, err = self.stor.insert(
            [Country(id=None, country="Raj", capital="Delhi")]
        )
        self.assertIs(err, None), f"insert error: {repr(err)}"
        self.assertEqual(count, 1), f"inserted rows count != 1"

    def test7_update(self):
        india = Country(None, "India", "New-Delhi")
        count, err = self.stor.update([india], where=(self.t.country == "Raj"))
        self.assertIs(err, None), f"update error: {repr(err)}"
        self.assertEqual(count, 1), f"updated rows != 1 ({count})"
        updated_india, sel_err = self.stor.select_one(
            where=(self.t.capital == "New-Delhi")
        )
        self.assertIs(sel_err, None), f"select error: {repr(err)}"
        self.assertEqual(
            Country(None, "India", "New-Delhi"), updated_india
        ), f"unexpected india: {india}, capital should be 'New-Delhi'"

    def test8_delete(self):
        india, err = self.stor.select_one(where=(self.t.country == "India"))
        self.assertIs(err, None), f"select error: {repr(err)}"
        self.assertIsInstance(india, Country), f"india should be coutry"
        count, err = self.stor.delete(where=(self.t.id == india.id))
        self.assertIs(err, None), f"delete error: {repr(err)}"
        self.assertEqual(count, 1), f"deleted rows != 1 ({count})"


if __name__ == "__main__":
    unittest.main()
