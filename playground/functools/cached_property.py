from functools import cached_property


class CachedPropertyTest:
    def __init__(self, n) -> None:
        self.n = n
        self.count = 0

    @cached_property
    def result(self) -> int:
        self.count += 1
        self.n = self.n << self.n
        return self.n


if __name__ == "__main__":
    t = CachedPropertyTest(1)
    assert t.result == 2
    assert t.result == 2
    assert t.count == 1
    del t.result
    assert t.result == 8
    assert t.result == 8
    assert t.count == 2
    print("result: %d, count: %d" % (t.result, t.count))
