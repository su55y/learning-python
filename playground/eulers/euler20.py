from functools import reduce

print(
    """n! means n * (n - 1) * ... * 3 * 2 * 1.
For example, 10! = 10 * 9 * ... * 3 * 2 * 1 = 3628800,
and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.
Find the sum of the digits in the number 100!.

expected result: 648
"""
)

s = str(reduce(lambda p, n: p * n, range(1, 101)))
print("result:", reduce(lambda p, n: p + int(s[n]), range(len(s)), 0))
