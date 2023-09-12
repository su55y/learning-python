import unittest

from mutable_mapping import Map


class TestMutableMapping(unittest.TestCase):
    # Mapping methods
    def test_contains(self):
        map = Map(a=1)
        self.assertTrue("a" in map)

    def test_keys(self):
        map = Map({"a": 1}, b=52)
        self.assertEqual(map.keys(), {"a", "b"})

    def test_items(self):
        map = Map({"a": 1}, b=52)
        self.assertEqual(map.items(), {("a", 1), ("b", 52)})

    def test_values(self):
        map = Map([("a", 1)], b=52)
        self.assertEqual(set(map.values()), {1, 52})

    def test_get(self):
        map = Map(a=1)
        self.assertEqual(map.get("a"), 1)
        self.assertIs(map.get("b"), None)

    def test_comparsion(self):
        map = Map(a=1)
        self.assertEqual(map, {"a": 1})
        self.assertNotEqual(map, {"b": 52})

    # MutableMapping methods
    def test_pop(self):
        map = Map(a=1)
        self.assertEqual(map.pop("a"), 1)
        self.assertEqual(len(map), 0)

    def test_pop_items(self):
        map = Map(a=1)
        self.assertEqual(map.popitem(), ("a", 1))
        self.assertEqual(len(map), 0)

    def test_clear(self):
        map = Map(a=1)
        map.clear()
        self.assertEqual(len(map), 0)

    def test_update(self):
        map = Map(a=1, b=42)
        map.update(Map([("b", 52)], c=4))
        self.assertEqual(map, {"a": 1, "b": 52, "c": 4})

    def test_setdefault(self):
        map = Map()
        self.assertEqual(map.setdefault("a", 1), 1)
        self.assertEqual(len(map), 1)
