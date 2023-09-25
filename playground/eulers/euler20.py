print(
    """n! means n * (n - 1) * ... * 3 * 2 * 1.
For example, 10! = 10 * 9 * ... * 3 * 2 * 1 = 3628800,
and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.
Find the sum of the digits in the number 100!.

expected result: 648
"""
)


n = 1
for i in range(2, 101):
    n *= i
result = 0
for i in range(len(str(n))):
    result += int(str(n)[i])

print("result", result)
