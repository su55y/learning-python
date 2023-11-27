print(
    """The number, 197, is called a circular prime because all rotations of the
digits: 197, 971, and 719, are themselves prime. There are thirteen such primes
below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.
How many circular primes are there below one million?

expected result: 55
"""
)

LIMIT = 1_000_000
arr = [False for _ in range(LIMIT)]
arr[1] = True
prime = 3
res = 13
lc = 0
while True:
    for i in range(prime*2, LIMIT, prime):
        arr[i] = True
    i = prime+2
    while i < LIMIT and arr[i]:
        i+=2
    if i < LIMIT:
        s = "%d" % (prime := i)
        skip = False
        if prime > 100:
            lc = 1
            for i in range(len(s)-1):
                s = s[1:]+s[0]
                tmp = int(s)
                if tmp > prime:
                    skip = True
                    break
                elif not arr[tmp] and tmp%2 != 0:
                    lc+=1
                else:
                    skip = True
                    break
        if not skip:
            res += lc
    else:
        break
print("result:", res)
