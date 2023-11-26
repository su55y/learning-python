print(
    """The first two consecutive numbers to have two distinct prime factors are:
    14 = 2 * 7
    15 = 3 * 5.
The first three consecutive numbers to have three distinct prime factors are:
    644 = 2^2 * 7 * 23
    645 = 3 * 5 * 43
    646 = 2 * 17 * 19.
Find the first four consecutive integers to have four distinct prime factors
each. What is the first of these numbers?

expected result: 134043 
"""
)

LIMIT = 1_000_000
arr = [False for _ in range(LIMIT)]
arr[0], arr[1] = True, True
count, prime = 2, 3
while True:
    for i in range(2*prime, LIMIT, prime):
        arr[i] = True
    i = prime+2
    while i < LIMIT and arr[i]:
        i+=2
    if i < LIMIT:
        prime = i
        count+=1
    else:
        break

primes = [0 for _ in range(count)]
primes[0] = 2
index = 1
for i in range(3, LIMIT, 2):
    if not arr[i]:
        primes[index] = i
        index+=1

c_count, d_count = 0, 0
for i in range(646, LIMIT):
    c_count = 0
    for j in range(i, i+4):
        d_count = 0
        if not arr[j] and j%2 != 0:
            break
        tmp = j
        break_to_outer = False
        for k in range(count):
            if (not arr[tmp] and tmp%2 != 0) or (tmp%primes[k] == 0):
                d_count+=1
                if d_count == 4:
                    c_count+=1
                    if c_count == 4:
                        print("result:", i)
                        exit(0)
                    break
                elif not arr[tmp] and tmp%2 != 0:
                    break_to_outer = True
                    break
                while tmp%primes[k] == 0:
                    tmp //= primes[k]
        if break_to_outer:
            break
