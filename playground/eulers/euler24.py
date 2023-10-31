print(
    """A permutation is an ordered arrangement of objects. For example, 3124 is
one possible permutation of the digits 1, 2, 3 and 4. If all of the
permutations are listed numerically or alphabetically, we call it lexicographic
order. The lexicographic permutations of 0, 1 and 2 are:
    012 021 102 120 201 210
What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5,
6, 7, 8 and 9?

expected result: 2783915460"""
)


used = [False for _ in range(10)]
remaining = 999_999
res = ""
for i in range(9, 0, -1):
    perm = 1
    for j in range(i, 0, -1):
        perm*= j
    index, remaining = divmod(remaining, perm)
    j = 0
    while j < index or used[j]:
        if used[j]:
            index += 1
        j+=1
    used[j] = True
    res += "%s" % j
res += "%s" % remaining
print("result:", res)
