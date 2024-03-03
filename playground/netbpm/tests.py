from pathlib import Path
import random
import unittest

from netpbm import Netpbm, MagicNumber


class TestNetpbm(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dimensions = 80, 80
        w, h = cls.dimensions
        cls.pixels_sum = w * h
        cls.images_dir = Path("/tmp")
        cls.max_pgm_value = 16
        cls.pgm_colors = tuple(range(cls.max_pgm_value + 1))
        cls.max_ppm_value = 255
        cls.ppm_colors = ((0xFF, 0x00, 0xFF), (0xFF, 0xFF, 0x00), (0x00, 0xFF, 0xFF))

    def test_pbm(self):
        w, h = self.dimensions
        data = tuple(tuple(random.choice([0, 1]) for _ in range(w)) for _ in range(h))
        path = self.images_dir.joinpath("test.pbm")
        err = Netpbm(MagicNumber.P1, path, data, (w, h)).write()
        self.assertIsNone(err)

    def test_pgm(self):
        w, h = self.dimensions
        data = tuple(
            tuple(random.choice(self.pgm_colors) for _ in range(w)) for _ in range(h)
        )
        path = self.images_dir.joinpath("test.pgm")
        err = Netpbm(MagicNumber.P2, path, data, (w, h), self.max_pgm_value).write()
        self.assertIsNone(err)

    def test_ppm(self):
        data = tuple(random.choice(self.ppm_colors) for _ in range(self.pixels_sum))
        path = self.images_dir.joinpath("test.ppm")
        err = Netpbm(
            MagicNumber.P3, path, data, self.dimensions, self.max_ppm_value
        ).write()
        self.assertIsNone(err)

    def test_pbm_bin(self):
        data = tuple(random.choice([0, 1]) for _ in range(self.pixels_sum))
        path = self.images_dir.joinpath("test.pbmb")
        err = Netpbm(MagicNumber.P4, path, data, self.dimensions).write()
        self.assertIsNone(err)

    def test_broken_pbm_bin(self):
        args = lambda d: (MagicNumber.P4, "/tmp/test_pbmb_broken.pbm", d, (0, 0))
        self.assertIsNotNone(Netpbm(*args([2])).write())
        self.assertIsNotNone(Netpbm(*args((i for i in range(1)))).write())

    def test_pgm_bin(self):
        data = bytearray(random.choice(self.pgm_colors) for _ in range(self.pixels_sum))
        path = self.images_dir.joinpath("test.pgmb")
        err = Netpbm(
            MagicNumber.P5, path, data, self.dimensions, self.max_pgm_value
        ).write()
        self.assertIsNone(err)

    def test_pgm_bin_from_sequence(self):
        data = tuple(random.choice(self.pgm_colors) for _ in range(self.pixels_sum))
        path = self.images_dir.joinpath("test2.pgmb")
        err = Netpbm(
            MagicNumber.P5, path, data, self.dimensions, self.max_pgm_value
        ).write()
        self.assertIsNone(err)

    def test_ppm_bin(self):
        colors = (b"\xff\x00\xff", b"\xff\xff\x00", b"\x00\xff\xff")
        data = bytearray(
            b"".join(random.choice(colors) for _ in range(self.pixels_sum))
        )
        path = self.images_dir.joinpath("test.ppmb")
        err = Netpbm(
            MagicNumber.P6, path, data, self.dimensions, self.max_ppm_value
        ).write()
        self.assertIsNone(err)

    def test_ppm_bin_from_sequence(self):
        data = [random.choice(self.ppm_colors) for _ in range(self.pixels_sum)]
        path = self.images_dir.joinpath("test2.ppmb")
        err = Netpbm(
            MagicNumber.P6, path, data, self.dimensions, self.max_ppm_value
        ).write()
        self.assertIsNone(err)
