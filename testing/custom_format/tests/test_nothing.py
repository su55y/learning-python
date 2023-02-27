import unittest


class TestNothing(unittest.TestCase):
    def test1_always_pass(self):
        self.assertTrue(1, "should be true")

    def test2_always_fail(self):
        self.assertTrue(0, "should be true")

    def test3_always_error(self):
        raise Exception("some test error")
