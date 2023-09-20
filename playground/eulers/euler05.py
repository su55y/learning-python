print(
    """
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

expected result: 232792560
"""
)


def is_not_prime(n):
    for x in range(2, n):
        if n % x == 0:
            return True


primes = [n for n in range(2, 20) if not is_not_prime(n)]

result = 1

for i in range(len(primes)):
    divisor = primes[i]
    while divisor <= 20:
        divisor *= primes[i]
    divisor /= primes[i]
    result *= divisor

print(result)
