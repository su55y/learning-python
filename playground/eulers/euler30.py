print(
    """Surprisingly there are only three numbers that can be written as the
sum of fourth powers of their digits:
    1634 = 1^4 + 6^4 + 3^4 + 4^4
    8208 = 8^4 + 2^4 + 0^4 + 8^4
    9474 = 9^4 + 4^4 + 7^4 + 4^4

The sum of these numbers is 1634 + 8208 + 9474 = 19316.
Find the sum of all the numbers that can be written as the sum of fifth powers
of their digits.

expected result: 443839
"""
)

def sum5pows(n: int) -> int:
    sum = 0
    while n > 0:
        n, rest = divmod(n, 10)
        sum += rest**5
    return sum

sum = 0
for i in range(22, 9**5 * 4):
    if i == sum5pows(i):
        sum+=i
print("result:", sum)
