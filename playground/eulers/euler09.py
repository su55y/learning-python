import math

print(
    """
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which, a^2 + b^2 = c^2.
For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2. There exists exactly one Pythagorean triplet for which a + b + c = 1000. Find the product abc.

expected result: 31875000"""
)

for a in range(1, 501):
    for b in range(a, 501):
        if (c := math.sqrt(n := a**2 + b**2)) ** 2 == n and a + b + c == 1000:
            print("result:", a * b * c)
            exit(0)
