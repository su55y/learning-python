import unittest

from . import country_test, storage_test


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(country_test.CountriesTest))
    suite.addTests(loader.loadTestsFromTestCase(storage_test.CountriesStorageTest))
    return suite


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite())


if __name__ == "__main__":
    main()
