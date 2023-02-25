import unittest

from . import country_test, storage_test
from sys import argv


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(country_test.CountriesTest))
    suite.addTests(loader.loadTestsFromTestCase(storage_test.CountriesStorageTest))
    return suite


def main():
    verbosity = 2 if "-v" in argv[1:] else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite())


if __name__ == "__main__":
    main()
