print(
    """The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17. Find the sum of
all the primes below two million.

expected result: 142913828922
"""
)

LIMIT = 2_000_000
arr = [False for _ in range(LIMIT)]
arr[0], arr[1] = True, True
res, prime = 5, 3
while True:
    for i in range(prime * 2, LIMIT, prime):
        arr[i] = True
    i = prime + 2
    while i < LIMIT and arr[i]:
        i += 2
    if i < LIMIT:
        prime = i
        res += i
    else:
        break
print("result:", res)
