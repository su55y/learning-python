#!/usr/bin/env -S python3 -u

from itertools import takewhile, count
from functools import reduce

print(
    """
Each new term in the Fibonacci sequence is generated by adding the previous two terms. By starting with 1 and 2, the first 10 terms will be:
    1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
By considering the terms in the Fibonacci sequence whose values do not exceed four million, find the sum of the even-valued terms.
(https://projecteuler.net/problem=2)

expected result: 4613732
"""
)

cache = {0: 0, 1: 1}
LIMIT = 4_000_000


def fibonacci_of(n) -> int:
    if n in cache:
        return cache[n]
    cache[n] = fibonacci_of(n - 1) + fibonacci_of(n - 2)

    return cache[n]


print(
    "result:",
    reduce(
        lambda p, n: p + n if n % 2 == 0 else p,
        [cache[i] for i in takewhile(lambda n: fibonacci_of(n) < LIMIT, count())],
    ),
)
