print(
    """The number 3797 has an interesting property. Being prime itself, it is
possible to continuously remove digits from left to right, and remain prime at
each stage: 3797, 797, 97, and 7. Similarly we can work from right to left:
3797, 379, 37, and 3.
Find the sum of the only eleven primes that are both truncatable from left to
right and right to left.
NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

expected result: 748317
"""
)

LIMIT = 1_000_000
arr = [False for _ in range(LIMIT)]
left, right = arr[:], arr[:]
arr[0], arr[1], arr[6], arr[9] = True, True, True, True
for i in [2, 3, 5, 7]:
    left[i] = True
    right[i] = True
for x in [3, 5, 7]:
    for i in range(x*2, LIMIT, x):
        arr[i] = True

c, sum = 0, 0
prime = 11
while True:
    if right[prime//10]:
        right[prime] = True
    if left[int(f"{prime}"[1:])]:
        left[prime] = True
        if right[prime]:
            sum += prime
            if (c := c+1) == 11:
                print("result:", sum)
                exit(0)
    for i in range(prime*2, LIMIT, prime):
        arr[i] = True
    i = prime+2
    while i < LIMIT and arr[i]:
        i+=2
    if i < LIMIT:
        prime = i
    else:
        exit(1)
