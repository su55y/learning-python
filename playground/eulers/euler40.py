from itertools import count

print(
    """An irrational decimal fraction is created by concatenating the positive
integers:
    0.12345678910*1*112131415161718192021...
It can be seen that the 12th digit of the fractional part is 1.
If d{n} represents the n_th digit of the fractional part, find the value of the
following expression.
    d{1} * d{10} * d{100} * d{1000} * d{10000} * d{100000} * d{1000000}

expected result: 210
"""
)

i = (i for i in count(1))
c, lim, res = 0, 10, 1
while lim < 1_000_001:
    if (c := c + len(s := str(next(i)))) >= lim:
        res *= int(s[len(s) - (c-lim)-1: len(s)-(c-lim)])
        lim*=10
print("result:", res)
