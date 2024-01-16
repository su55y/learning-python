import itertools as it

print(
    """The arithmetic sequence, 1487, 4817, 8147, in which each of the terms
increases by 3330, is unusual in two ways: (i) each of the three terms are
prime, and, (ii) each of the 4-digit numbers are permutations of one another.
There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes,
exhibiting this property, but there is one other 4-digit increasing sequence.
What 12-digit number do you form by concatenating the three terms in this
sequence?

expected result: 296962999629
"""
)


def is_perm(x: int, y: int) -> bool:
    s1, s2 = str(x), str(y)
    for i in range(len(s1)):
        if s2.find(s1[i : i + 1]) < 0 or s1.find(s2[i : i + 1]) < 0:
            return False
    return True


LIMIT = 10_000
arr = [False for _ in range(LIMIT)]
prime = 2
while True:
    for i in range(2 * prime, LIMIT, prime):
        arr[i] = True
    i = prime + 1
    while i < LIMIT and arr[i]:
        i += 1
    if i < LIMIT:
        prime = i
    else:
        break

for i, j in it.combinations(range(1000, LIMIT), 2):
    if (
        i != 1487
        and not arr[i]
        and not arr[j]
        and is_perm(i, j)
        and 2 * j - i < LIMIT
        and not arr[2 * j - i]
        and is_perm(i, 2 * j - i)
    ):
        print("result:", "%d%d%d" % (i, j, 2 * j - i))
        exit(0)
