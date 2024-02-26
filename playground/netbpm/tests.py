import random
import unittest

from netpbm import Netpbm, MagicNumber


class TestNetpbm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dimensions = 1920, 1080

    def test_pbm(self):
        colors = (0x00, 0x01)
        w, h = self.dimensions
        data = (tuple(random.choice(colors) for _ in range(w)) for _ in range(h))
        err = Netpbm(MagicNumber.P1, "/tmp/test.pbm", data, (w, h)).write()
        self.assertIsNone(err)

    def test_pgm(self):
        max_value = 16
        colors = tuple(range(max_value + 1))
        w, h = self.dimensions
        data = (tuple(random.choice(colors) for _ in range(w)) for _ in range(h))
        err = Netpbm(MagicNumber.P2, "/tmp/test.pgm", data, (w, h), max_value).write()
        self.assertIsNone(err)

    def test_ppm(self):
        max_value = 0xFF
        colors = ((0xFF, 0x00, 0xFF), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0xFF))
        w, h = self.dimensions
        data = (random.choice(colors) for _ in range(w * h))
        err = Netpbm(MagicNumber.P3, "/tmp/test.ppm", data, (w, h), max_value).write()
        self.assertIsNone(err)
