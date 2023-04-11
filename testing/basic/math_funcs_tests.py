import unittest

from math_funcs import count_sum


class TestMathFuncs(unittest.TestCase):
    def test_sum_list(self):
        self.assertEqual(count_sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(count_sum((1, 2, 3)), 6, "Should be 6")

    def test_sum_set(self):
        self.assertEqual(count_sum({1, 2, 3}), 6, "Should be 6")


if __name__ == "__main__":
    unittest.main()
