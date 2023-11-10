print(
    """We shall say that an n-digit number is pandigital if it makes use of all
the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1
through 5 pandigital.
The product 7254 is unusual, as the identity, 39 * 186 = 7254, containing
multiplicand, multiplier, and product is 1 through 9 pandigital.
Find the sum of all products whose multiplicand/multiplier/product identity can
be written as a 1 through 9 pandigital.
HINT: Some products can be obtained in more than one way so be sure to only
include it once in your sum.

expected result: 45228
"""
)


def is_pandigital(m1, m2, res):
    if len(s := f"{m1}{m2}{res}") != 9:
        return False
    for i in range(1, 10):
        if not (f"{i}" in s):
            return False
    return True

sp = set()
for i in range(1, 200):
    for j in range(1, 5000):
        if is_pandigital(i, j, p := i*j):
            sp.add(p)


print("result:", sum(sp))
