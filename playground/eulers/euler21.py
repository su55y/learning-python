import math

print(
    """Let d(n) be defined as the sum of proper divisors of n (numbers less
than n which divide evenly into n).
If d(a) = b and d(b) = a, where a != b, then a and b are an amicable pair and
each of a and b are called amicable numbers. For example, the proper divisors
of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284.
The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.
Evaluate the sum of all the amicable numbers under 10000.

expected result: 31626"""
)

def divisors_sum(inp: int) -> int:
    sum = 0
    for i in range(1, int(math.sqrt(abs(inp)))+1):
        if inp%i == 0:
            if i == inp//i:
                sum += i
            else:
                sum += i + (inp / i)
    return int(sum - inp)

sum, j = 0, 0
for i in range(1, 10_000):
    j = divisors_sum(i)
    if i == divisors_sum(j) and i != j:
        sum += i

print("result:", sum)
