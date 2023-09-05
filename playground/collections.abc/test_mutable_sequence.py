import unittest

from mutable_sequence import Array


class TestMutableSequence(unittest.TestCase):
    # Sequence methods
    def test_contains(self):
        arr = Array(2).fill([1])
        self.assertTrue(1 in arr)
        self.assertTrue(None in arr)
        self.assertTrue(2 not in arr)

    def test_iter(self):
        arr = Array(3).fill([1, 2])
        control_list = [1, 2, None]
        for i, v in enumerate(arr):
            self.assertIn(i, {0, 1, 2})
            self.assertIn(v, {1, 2, None})
            self.assertEqual(v, control_list[i])

    def test_reversed(self):
        arr = Array(3).fill([1, 2])
        control_list = [None, 2, 1]
        for i, v in enumerate(reversed(arr)):
            self.assertIn(i, {0, 1, 2})
            self.assertIn(v, {1, 2, None})
            self.assertEqual(v, control_list[i])

    def test_index(self):
        arr = Array(3).fill([1, 2, 2])
        self.assertEqual(arr.index(2), 1)
        self.assertEqual(arr.index(2, 2), 2)
        self.assertRaises(ValueError, arr.index, 3)

    def test_count(self):
        arr = Array(3).fill([1, 2, 2])
        self.assertEqual(arr.count(2), 2)
        self.assertEqual(arr.count(1), 1)
        self.assertEqual(arr.count(3), 0)

    # MutableSequence methods
    def test_append(self):
        arr = Array()
        arr.append(1)
        self.assertEqual(list(arr), [1])

    def test_reverse(self):
        arr = Array(3).fill([1, 2, 3])
        arr.reverse()
        self.assertEqual(list(arr), [3, 2, 1])

    def test_extend(self):
        arr = Array()
        arr.extend([1])
        self.assertEqual(list(arr), [1])

    def test_pop(self):
        arr = Array(3).fill([1, 2, 3])
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr.pop(), 3)
        self.assertEqual(len(arr), 2)
        self.assertNotIn(3, arr)

    def test_remove(self):
        arr = Array(3).fill([1, 2, 3])
        self.assertIn(2, arr)
        self.assertEqual(3, len(arr))
        arr.remove(2)
        self.assertNotIn(2, arr)
        self.assertEqual(2, len(arr))

    def test_iadd(self):
        arr = Array(2).fill([1, 2])
        arr += [3]
        self.assertEqual(list(arr), [1, 2, 3])

    # MutableSequence abstract methods (__getitem__, __setitem__, __delitem__, __len__, insert)
    def test_getitem(self):
        arr = Array(1)
        self.assertIs(arr[0], None)
        arr[0] = 42
        self.assertEqual(arr[0], 42)
        self.assertEqual(len(arr), 1)
        del arr[0]
        self.assertEqual(len(arr), 0)
        arr.insert(0, 42)
        self.assertEqual(arr[0], 42)
