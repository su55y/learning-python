from itertools import count
import math

print(
    """It was proposed by Christian Goldbach that every odd composite number
can be written as the sum of a prime and twice a square.
    9 = 7 + 2 * 1^2
    15 = 7 + 2 * 2^2
    21 = 3 + 2 * 3^2
    25 = 7 + 2 * 3^2
    27 = 19 + 2 * 2^2
    33 = 31 + 2 * 1^2
It turns out that the conjecture was false.
What is the smallest odd composite that cannot be written as the sum of a prime
and twice a square?

expected result: 5777
"""
)

arr = [False for _ in range(1_000_000)]
arr[2] = True
for i in count(3, 2):
    composite = False
    for j in range(2, i):
        if arr[j] and i%j == 0 and (composite := True):
            break
    if composite:
        found = False
        for j in range(2, i):
            if arr[j]:
                if (n:=i-j)%2 == 0 and int(math.sqrt(int(n/2)))**2 == n//2:
                    found = True
                    break
        if not found:
            print("result:", i)
            exit(0)
    else:
        arr[i] = True
