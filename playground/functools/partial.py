from functools import partial


def pow(exponent: int, /, base: int):
    return base**exponent


def test(a, b):
    print(f"{a=}, {b=}")


if __name__ == "__main__":
    pow_of_two = partial(pow, base=2)
    assert pow_of_two(8) == 256
    t = partial(test, a="first a")
    # no lint from pyright 🤔
    t("second a", a="third a")  # TypeError: test() got multiple values for argument 'a'
