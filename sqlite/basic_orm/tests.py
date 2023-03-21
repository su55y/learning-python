import logging
import os.path
import unittest

import sqlalchemy
import sqlalchemy.orm


from models import Base, Country

DB_FILE = "test.db"
LOG_FMT = "[%(levelname)s] %(message)s"
LOG_FILE = "tests.log"
LOGGER = "sqlalchemy"


def configured_logger():
    logging.getLogger(LOGGER).setLevel(logging.INFO)
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter(LOG_FMT))
    logging.getLogger(LOGGER).addHandler(fh)
    return logging.getLogger(LOGGER)


class BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = sqlalchemy.create_engine(f"sqlite:///{DB_FILE}")
        cls.log = configured_logger()
        Base.metadata.create_all(cls.engine)
        cls.make_session = sqlalchemy.orm.sessionmaker(
            bind=cls.engine, expire_on_commit=False
        )

        cls.insert_data = [
            Country(name="Peru", capital="Lima"),
            Country(**{"name": "UK", "capital": "London"}),
        ]

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    @classmethod
    def setUp(cls):
        cls.rows = None
        cls.count = None

    def test1_insert(self):
        with self.make_session() as s:
            s.add_all(self.insert_data)
            s.commit()
            self.count = s.query(Country).count()
        self.assertEqual(self.count, len(self.insert_data))

    def test2_select(self):
        with self.make_session() as s:
            self.rows = s.query(Country).all()
        self.assertEqual(self.rows, self.insert_data)

    def test2_select_query(self):
        query = sqlalchemy.select(Country)
        with self.make_session() as s:
            self.rows = s.scalars(query).all()
        self.assertEqual(self.rows, self.insert_data)

    def test2_select_with_conn(self):
        query = sqlalchemy.select(Country)
        with self.engine.begin() as conn:
            cur = conn.execute(query)
            self.rows = [Country(name=n, capital=c) for n, c in cur.all()]
        self.assertEqual(self.rows, self.insert_data)
