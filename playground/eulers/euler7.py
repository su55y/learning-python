print(
    """
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13,
we can see that the 6th prime is 13. What is the 10,001st prime number?

expected result: 104743
"""
)

from math import floor


def is_prime(n):
    for x in range(2, floor(n**0.5) + 1):
        if n % x == 0:
            return False
    return True


if __name__ == "__main__":
    primes = []
    i = 2
    while len(primes) < 10_001:
        if is_prime(i):
            primes.append(i)
        i += 1

    print(primes.pop())
