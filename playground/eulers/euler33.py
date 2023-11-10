print(
    """The fraction 49/98 is a curious fraction, as an inexperienced
mathematician in attempting to simplify it may incorrectly believe that 49/98 =
4/8, which is correct, is obtained by cancelling the 9s.
We shall consider fractions like, 30/50 = 3/5, to be trivial examples.
There are exactly four non-trivial examples of this type of fraction, less than
one in value, and containing two digits in the numerator and denominator.
If the product of these four fractions is given in its lowest common terms,
find the value of the denominator.

expected result: 100
"""
)

res = 1
for i in range(1, 10):
    for j in range(1, i):
        for k in range(1, j):
            ki = 10*k + i
            ij = 10*i + j
            if ki*j == ij*k:
                res *= ij / ki

print("result:", int(res))
