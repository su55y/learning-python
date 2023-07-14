import logging
import unittest

import sqlalchemy
import sqlalchemy.orm


from models import Base, Country

LOG_FILE = "tests.log"
INSERT_DATA = [
    Country(name="Peru", capital="Lima"),
    Country(**{"name": "UK", "capital": "London"}),
]


class BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = sqlalchemy.create_engine("sqlite:///:memory:")

        cls.log = logging.getLogger()
        fh = logging.FileHandler(LOG_FILE)
        fh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
        cls.log.addHandler(fh)

        Base.metadata.create_all(cls.engine)
        cls.make_session = sqlalchemy.orm.sessionmaker(
            bind=cls.engine, expire_on_commit=False
        )

    def test1_insert(self):
        with self.make_session() as s:
            s.add_all(INSERT_DATA)
            s.commit()
            count = s.query(Country).count()
        self.assertEqual(count, len(INSERT_DATA))

    def test2_select(self):
        with self.make_session() as s:
            rows = s.query(Country).all()
        self.assertEqual(rows, INSERT_DATA)

    def test2_select_query(self):
        query = sqlalchemy.select(Country)
        with self.make_session() as s:
            rows = s.scalars(query).all()
        self.assertEqual(rows, INSERT_DATA)

    def test2_select_with_conn(self):
        query = sqlalchemy.select(Country)
        with self.engine.begin() as conn:
            cur = conn.execute(query)
            countries = [Country(name=n, capital=c) for n, c in cur.all()]
        self.assertEqual(countries, INSERT_DATA)
