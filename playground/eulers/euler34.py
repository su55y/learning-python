print(
    """145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.
Find the sum of all numbers which are equal to the sum of the factorial of
their digits.
Note: As 1! = 1 and 2! = 2 are not sums they are not included.

expected result: 40730
"""
)

factorials = [0 for _ in range(10)]
factorials[0] = 1
for i in range(1, 10):
    factorials[i] = factorials[i-1] * i

pow10 = 10
limit = factorials[-1]
while limit > pow10:
    limit *= 2
    pow10 *= 10

sum = 0
for i in range(10, limit):
    lsum, j = 0, i
    while j > 9:
        lsum += factorials[j%10]
        j //= 10
    lsum += factorials[j]
    if i == lsum:
        sum += i

print("result:", sum)
