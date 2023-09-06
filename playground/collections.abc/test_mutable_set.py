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
