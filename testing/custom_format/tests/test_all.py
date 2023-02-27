import unittest

from .test_nothing import TestNothing
from .test_math_pkg import MathPkgTest
from .format import ResultFormat


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromTestCase(MathPkgTest))
    suite.addTests(loader.loadTestsFromTestCase(TestNothing))
    return suite


def main():
    runner = unittest.TextTestRunner(resultclass=ResultFormat, verbosity=0)
    runner.run(suite())


if __name__ == "__main__":
    main()
