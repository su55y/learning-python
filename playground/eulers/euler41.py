print(
    """We shall say that an $n$-digit number is pandigital if it makes use of
all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital
and is also prime.
What is the largest n-digit pandigital prime that exists?

expected result: 7652413
"""
)


def is_pandigital(n: int) -> bool:
    for i in range(1, len(s := "%d" % n) + 1):
        if str(i) not in s:
            return False
    return True


LIMIT = 87654322
a = [False for _ in range(LIMIT)]
a[0], a[1] = True, True
prime = 3
while True:
    for i in range(2 * prime, LIMIT, prime):
        a[i] = True
    i = prime + 2
    while i < LIMIT and a[i]:
        i += 2
    if i < LIMIT:
        prime = i
    else:
        break

for i in range(LIMIT - 1, 0, -2):
    if not a[i] and is_pandigital(i):
        print("result:", i)
        break
