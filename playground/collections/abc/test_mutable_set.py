import unittest

from mutable_set import Set


class TestMutableSet(unittest.TestCase):
    # Set methods
    def test_comparsion(self):
        s = Set({1, 2})
        self.assertTrue(s.isdisjoint({3, 4}))
        self.assertGreater(s, {2})
        self.assertGreaterEqual(s, {1, 2})
        self.assertLess(s, {1, 2, 3})
        self.assertLessEqual(s, {1, 2})
        self.assertNotEqual(s, {2})
        self.assertEqual(s, {1, 2})
        self.assertEqual(s & Set({2, 3}), {2})
        self.assertEqual(s | Set({2, 3}), {1, 2, 3})
        self.assertEqual(s - Set({2, 3}), {1})
        self.assertEqual(s ^ Set({2, 3}), {1, 3})

    # MutableSet methods
    def test_clear(self):
        s = Set({1, 2})
        s.clear()
        self.assertEqual(len(s), 0)

    def test_pop(self):
        s = Set({1, 2})
        self.assertEqual(s.pop(), 1)
        self.assertEqual(len(s), 1)

    def test_remove(self):
        s = Set({1, 2})
        s.remove(2)
        self.assertEqual(len(s), 1)
        self.assertEqual(s.pop(), 1)

    def test_increment_methods(self):
        s = Set({1, 2})
        s |= Set({2, 3})
        self.assertEqual(s, {1, 2, 3})
        s = Set({1, 2})
        s &= Set({2, 3})
        self.assertEqual(s, {2})
        s = Set({1, 2})
        s ^= Set({2, 3})
        self.assertEqual(s, {1, 3})
        s = Set({1, 2})
        s -= Set({2, 3})
        self.assertEqual(s, {1})
