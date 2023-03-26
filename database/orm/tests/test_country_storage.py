import logging
import unittest

from sqlalchemy.exc import NoResultFound

from database import init_db
from database.models import Country
from storage.country_storage import CountryStorage as stor

LOGGER = "sqlalchemy"
LOG_FILE = "tests.log"
LOG_FMT = "[%(levelname)s] %(message)s"


class TestCountryStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if err := init_db():
            raise err

        logging.getLogger(LOGGER).setLevel(logging.INFO)
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(logging.Formatter(LOG_FMT))
        logging.getLogger(LOGGER).addHandler(fh)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.insert_data = [
            Country(name="Peru", capital="Lima"),
            Country(name="UK", capital="London"),
        ]
        self.raj = Country(name="Raj", capital="Delhi")
        self.india = {"name": "India", "capital": "New Delhi"}

    def test1_insert_many(self):
        err = stor.insert_many(self.insert_data)
        self.assertIsNone(err)

    def test1_insert_one(self):
        err = stor.insert_one(self.raj)
        self.assertIsNone(err)

    def test2_select_all(self):
        counties, err = stor.select()
        self.assertIsNone(err)
        self.assertEqual(len(counties), 3)
        self.assertEqual(counties, [*self.insert_data, self.raj])

    def test3_update(self):
        india, select_err = stor.select_one(Country.name == "Raj")
        self.assertIsNone(select_err)
        self.assertIsNotNone(india)
        self.assertIsInstance(india, Country)
        err = stor.update(india.id, **self.india)
        self.assertIsNone(err)

    def test4_check_update(self):
        india, err = stor.select_one(Country.name == "India")
        self.assertIsNone(err)
        self.assertEqual(india, Country(name="India", capital="New Delhi"))

    def test5_delete(self):
        india, select_err = stor.select_one(Country.name == "India")
        self.assertIsNone(select_err)
        self.assertIsNotNone(india)
        self.assertIsInstance(india, Country)
        err = stor.delete(india.id)
        self.assertIsNone(err)

    def test6_select_not_found(self):
        _, err = stor.select_one(Country.name == "India")
        self.assertIsInstance(err, NoResultFound)


if __name__ == "__main__":
    unittest.main()
