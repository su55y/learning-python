import unittest

from math_pkg import integers


class MathPkgTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(integers.add(2, 2), 4, "should be 4")

    def test_sub(self):
        self.assertEqual(integers.sub(4, 2), 2, "should be 2")


if __name__ == "__main__":
    unittest.main()
