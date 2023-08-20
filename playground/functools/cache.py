from functools import cache, lru_cache

count = 0
count2 = 0


def counter():
    global count
    count += 1


def counter2():
    global count2
    count2 += 1


@cache
def factorial(n: int):
    counter()
    return 1 if not n else n * factorial(n - 1)


@lru_cache(maxsize=10)
def lfactorial(n: int):
    counter2()
    return 1 if not n else n * lfactorial(n - 1)


if __name__ == "__main__":
    print(", ".join(f"!{n} = {factorial(n)}" for n in range(1, 11)[::-1]))
    print(", ".join(f"!{n} = {lfactorial(n)}" for n in range(1, 11)[::-1]))
    print(f"calls count:\n- factorial: {count}\n- lfactorial: {count2}")
    assert (
        count
        == count2
        == factorial.cache_info().misses
        == lfactorial.cache_info().misses
    )
