import unittest

from country.country import Country


class CountriesTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.ukraine = Country(None, "Ukraine", "Kyiv")

    def test_equality(self):
        ukraine2 = Country(None, "Ukraine", "Kyiv")
        self.assertEqual(
            self.ukraine, ukraine2
        ), f"should be equal ({self.ukraine} != {ukraine2})"

    def test_str(self):
        self.assertEqual(
            str(self.ukraine), "Ukraine: Kyiv"
        ), f"invalid string repr ({self.ukraine})"


if __name__ == "__main__":
    unittest.main()
