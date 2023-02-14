import unittest
from math_funcs import sum


class TestSum(unittest.TestCase):
    def test_sum_list(self):
        self.assertEqual(sum.get_sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum.get_sum((1, 2, 3)), 6, "Should be 6")

    def test_sum_dict(self):
        self.assertEqual(sum.get_sum({1, 2, 3}), 6, "Should be 6")


if __name__ == "__main__":
    unittest.main()
