print(
    """2520 is the smallest number that can be divided by each of the numbers
from 1 to 10 without any remainder. What is the smallest positive number that
is evenly divisible by all of the numbers from 1 to 20?

expected result: 232792560
"""
)


def is_not_prime(n):
    for x in range(2, n):
        if n % x == 0:
            return True

LIMIT = 20
primes = [n for n in range(2, LIMIT) if not is_not_prime(n)]
res = 1

for i in primes:
    divisor = i
    while divisor <= LIMIT:
        divisor *= i
    divisor //= i
    res *= divisor

print("result:", res)
