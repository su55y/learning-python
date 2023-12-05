from itertools import count
import math

print(
    """By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13,
we can see that the 6th prime is 13. What is the 10,001st prime number?

expected result: 104743
"""
)


def is_prime(n):
    for x in range(2, math.floor(n**0.5) + 1):
        if n % x == 0:
            return
    return True


i = 0
res = 0
counter = count(2)
while i < 10_001:
    if is_prime(res := next(counter)):
        i+=1
print("result:", res)
