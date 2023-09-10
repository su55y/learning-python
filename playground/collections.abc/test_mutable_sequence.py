import unittest

from mutable_sequence import List


class TestMutableSequence(unittest.TestCase):
    # Sequence methods
    def test_contains(self):
        s = List([1])
        self.assertTrue(1 in s)
        self.assertTrue(2 not in s)

    def test_iter(self):
        s = List([1, 2])
        control_list = [1, 2]
        for i, v in enumerate(s):
            self.assertIn(i, {0, 1})
            self.assertIn(v, {1, 2})
            self.assertEqual(v, control_list[i])

    def test_reversed(self):
        s = List([1, 2])
        control_list = [2, 1]
        for i, v in enumerate(reversed(s)):
            self.assertIn(i, {0, 1})
            self.assertIn(v, {1, 2})
            self.assertEqual(v, control_list[i])

    def test_index(self):
        s = List([1, 2, 2])
        self.assertEqual(s.index(2), 1)
        self.assertEqual(s.index(2, 2), 2)
        self.assertRaises(ValueError, s.index, 3)

    def test_count(self):
        s = List([1, 2, 2])
        self.assertEqual(s.count(2), 2)
        self.assertEqual(s.count(1), 1)
        self.assertEqual(s.count(3), 0)

    # MutableSequence methods
    def test_append(self):
        s = List()
        s.append(1)
        self.assertEqual(list(s), [1])

    def test_reverse(self):
        s = List([1, 2, 3])
        s.reverse()
        self.assertEqual(list(s), [3, 2, 1])

    def test_extend(self):
        s = List()
        s.extend([1])
        self.assertEqual(list(s), [1])

    def test_pop(self):
        s = List([1, 2, 3])
        self.assertEqual(len(s), 3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(len(s), 2)
        self.assertNotIn(3, s)

    def test_remove(self):
        s = List([1, 2, 3])
        self.assertIn(2, s)
        self.assertEqual(3, len(s))
        s.remove(2)
        self.assertNotIn(2, s)
        self.assertEqual(2, len(s))

    def test_iadd(self):
        s = List([1, 2])
        s += [3]
        self.assertEqual(list(s), [1, 2, 3])

    # MutableSequence abstract methods (__getitem__, __setitem__, __delitem__, __len__, insert)
    def test_getitem(self):
        s = List([None])
        s[0] = 42
        self.assertEqual(s[0], 42)
        self.assertEqual(len(s), 1)
        del s[0]
        self.assertEqual(len(s), 0)
        s.insert(0, 42)
        self.assertEqual(s[0], 42)
