print(
    """The following iterative sequence is defined for the set of positive
integers:
    n -> n/2 (n is even)
    n -> 3n + 1 (n is odd)
Using the rule above and starting with 13, we generate the following sequence:
    13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1.
It can be seen that this sequence (starting at 13 and finishing at 1) contains
10 terms. Although it has not been proved yet (Collatz Problem), it is thought
that all starting numbers finish at 1.
Which starting number, under one million, produces the longest chain?
NOTE: Once the chain starts the terms are allowed to go above one million.

expected result: 837799
"""
)

LIMIT = 1_000_000
arr = [0 for _ in range(LIMIT)]
max, res = 0, 0

for i in range(1, LIMIT):
    j = i
    steps = 0
    while True:
        if j == 1:
            arr[i] = steps
            if steps > max:
                max, res = steps, i
            break
        elif j < i:
            steps += arr[j]
            arr[i] = steps
            if steps > max:
                max, res = steps, i
            break
        if j % 2 == 0:
            j //= 2
        else:
            j = j * 3 + 1
        steps += 1

print("result:", res)
