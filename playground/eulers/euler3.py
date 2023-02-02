#!/usr/bin/env -S python3 -u

print(
    """
The prime factors of 13195 are 5, 7, 13 and 29.
What is the largest prime factor of the number 600851475143 ?
(https://projecteuler.net/problem=3)

expected result: 6857
"""
)

def result() -> int:
    LIMIT = 600851475143
    i = 1
    while (i * i < LIMIT) and (i := i + 1):
        while LIMIT % i == 0:
            LIMIT /= i

    return round(LIMIT)

print("result:", result())
