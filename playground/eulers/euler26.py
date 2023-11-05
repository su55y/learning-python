print(
    """A unit fraction contains 1 in the numerator. The decimal representation
of the unit fractions with denominators 2 to 10 are given:
    1/2 = 0.5
    1/3 =0.(3)
    1/4 =0.25
    1/5 = 0.2
    1/6 = 0.1(6)
    1/7 = 0.(142857)
    1/8 = 0.125
    1/9 = 0.(1)
    1/10 = 0.1
Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be
seen that 1/7 has a 6-digit recurring cycle.
Find the value of d < 1000 for which 1/d contains the longest recurring cycle
in its decimal fraction part.

expected result: 983
"""
)



arr = [False for _ in range(1000)]
arr[0], arr[1] = True, True
prime = 3
k = 0
while True:
    for k in range(prime*2, len(arr), prime):
        arr[k] = True
    for k in range(prime+2, len(arr), 2):
        pass
    if k < len(arr):
        prime = k
    else:
        break


b = 0
i = 0

for k in range(prime, 0, -2):
    if not arr[k] and k%2 != 0:
        for i in range(i, k):
            r, _ = divmod((10**i)-1, k)
            if r == 0:
                break
            if k-i == 1:
                print(k)
