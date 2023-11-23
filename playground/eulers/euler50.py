print(
    """The prime 41, can be written as the sum of six consecutive primes:
    41 = 2 + 3 + 5 + 7 + 11 + 13.
This is the longest sum of consecutive primes that adds to a prime below
one-hundred. The longest sum of consecutive primes below one-thousand that adds
to a prime, contains 21 terms, and is equal to 953.
Which prime, below one-million, can be written as the sum of the most
consecutive primes?

expected result: 997651
"""
)

LIMIT = 1_000_000
arr = [False for _ in range(LIMIT)]
arr[0], arr[1] = True, True
prime = 3
while True:
    for i in range(2*prime, LIMIT, prime):
        arr[i] = True
    i = prime+2
    while i < LIMIT and arr[i]:
        i+=2
    if i < LIMIT:
        prime = i
    else:
        break

primes = [i for i in range(LIMIT) if not arr[i] and i%2 != 0]
primes.insert(0, 2)
res, max_count = 0, 0
for i in range(len(primes)):
    t, count = primes[i], 0
    for j in range(i+1, len(primes)):
        t+=primes[j]
        count+=1
        if t>(LIMIT-1):
            break
        if t%2 != 0 and not arr[t] and count > max_count:
            max_count = count
            res = t

print("result:", res)
