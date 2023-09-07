import unittest

from mutable_set import Set


class TestMutableSet(unittest.TestCase):
    # Set methods
    def test_comparsion(self):
        s = Set("hello world!")
        self.assertTrue(s.isdisjoint(set("sus")))
        self.assertGreater(s, set("hello"))
        self.assertGreaterEqual(s, set("world"))
        self.assertLess(s, set("hello world!?"))
        self.assertLessEqual(s, set("oh, hello world!?"))
        self.assertNotEqual(s, set("hi"))
        self.assertEqual(s, set("! ehodlrw"))
        # __and__
        self.assertEqual(s & Set("bye"), {"e"})
        self.assertEqual(Set("good") | Set("bye"), set("bdegoy"))
        self.assertEqual(Set("hello") - Set("world"), set("eh"))
        self.assertEqual(Set("hello") ^ Set("world"), set("edhrw"))

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
