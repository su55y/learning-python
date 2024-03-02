import random
import unittest

from netpbm import Netpbm, MagicNumber


class TestNetpbm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dimensions = 80, 80

    def test_pbm(self):
        colors = (0x00, 0x01)
        w, h = self.dimensions
        data = tuple(tuple(random.choice(colors) for _ in range(w)) for _ in range(h))
        err = Netpbm(MagicNumber.P1, "/tmp/test.pbm", data, (w, h)).write()
        self.assertIsNone(err)

    def test_pgm(self):
        max_value = 16
        colors = tuple(range(max_value + 1))
        w, h = self.dimensions
        data = tuple(tuple(random.choice(colors) for _ in range(w)) for _ in range(h))
        err = Netpbm(MagicNumber.P2, "/tmp/test.pgm", data, (w, h), max_value).write()
        self.assertIsNone(err)

    def test_ppm(self):
        max_value = 0xFF
        colors = ((0xFF, 0x00, 0xFF), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0xFF))
        w, h = self.dimensions
        data = tuple(random.choice(colors) for _ in range(w * h))
        err = Netpbm(MagicNumber.P3, "/tmp/test.ppm", data, (w, h), max_value).write()
        self.assertIsNone(err)

    def test_pbm_bin(self):
        colors = (0, 1)
        w, h = self.dimensions
        data = tuple(random.choice(colors) for _ in range(w * h))
        err = Netpbm(MagicNumber.P4, "/tmp/testb.pbm", data, (w, h)).write()
        self.assertIsNone(err)

    def test_broken_pbm_bin(self):
        args = lambda d: (MagicNumber.P4, "/tmp/testbb.pbm", d, (0, 0))
        self.assertIsNotNone(Netpbm(*args([2])).write())
        self.assertIsNotNone(Netpbm(*args((i for i in range(1)))).write())

    def test_ppm_bin(self):
        max_value = 0xFF
        colors = ((0xFF, 0x00, 0xFF), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0xFF))
        colors = (b"\xff\x00\xff", b"\xff\xff\x00", b"\x00\xff\xff")
        w, h = self.dimensions
        data = bytearray(b"".join(random.choice(colors) for _ in range(w * h)))
        err = Netpbm(MagicNumber.P6, "/tmp/testb.ppm", data, (w, h), max_value).write()
        self.assertIsNone(err)

    def test_ppm_bin_from_sequence(self):
        max_value = 0xFF
        colors = ((0xFF, 0x00, 0xFF), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0xFF))
        w, h = self.dimensions
        data = [random.choice(colors) for _ in range(w * h)]
        err = Netpbm(MagicNumber.P6, "/tmp/testb2.ppm", data, (w, h), max_value).write()
        self.assertIsNone(err)
