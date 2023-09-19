print(
    """
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
Find the sum of all the primes below two million.
(https:#projecteuler.net/problem=10)

expected result: 142913828922
"""
)

flags = [False for _ in range(2_000_000)]
flags[0], flags[1] = True, True
sum, prime = 5, 3
k = 0
while True:
    for k in range(prime * 2, len(flags), prime):
        flags[k] = True
    k = prime + 2
    while k < len(flags) and flags[k]:
        k += 2
    if k < len(flags):
        prime = k
        sum += k
    else:
        break
print("result:", sum)
