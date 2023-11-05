from functools import reduce
import math

print(
    """A perfect number is a number for which the sum of its proper divisors
is exactly equal to the number. For example, the sum of the proper divisors of
28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.
A number n is called deficient if the sum of its proper divisors is less than
n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest
number that can be written as the sum of two abundant numbers is 24.
By mathematical analysis, it can be shown that all integers greater than 28123
can be written as the sum of two abundant numbers. However, this upper limit
cannot be reduced any further by analysis even though it is known that the
greatest number that cannot be expressed as the sum of two abundant numbers is
less than this limit. Find the sum of all the positive integers which cannot be
written as the sum of two abundant numbers.

expected result: 4179871
"""
)


def divisors_sum(inp: int) -> int:
    sum = 0
    for i in range(1, int(math.sqrt(inp)) + 1):
        if inp%i == 0:
            if i == inp//i:
                sum += i
            else:
                sum += i + (inp // i)
    return sum - inp

LIMIT = 28124
writables = [False for _ in range(LIMIT)]
for i, a in enumerate(abundants := [i for i in range(1, LIMIT) if i < divisors_sum(i)]):
    for b in abundants[i:]:
        if (sum := a + b) < LIMIT:
            writables[sum] = True

print("result:", reduce(lambda p, n: p if writables[n] else p+n, range(1, LIMIT), 0))
