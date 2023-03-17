import unittest
from sys import argv

from .test_storage import StorageTest
from .test_person_storage import PersonStorageTest


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(StorageTest))
    suite.addTests(loader.loadTestsFromTestCase(PersonStorageTest))
    return suite


if __name__ == "__main__":
    verbosity = 2 if "-v" in argv[1:] else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    runner.run(suite())
