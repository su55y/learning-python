print(
    """The prime factors of 13195 are 5, 7, 13 and 29.
What is the largest prime factor of the number 600851475143?

expected result: 6857
"""
)


res = 600851475143
i = 1
while (i := i + 1) ** 2 < res:
    while res % i == 0:
        res //= i
print("result:", res)
