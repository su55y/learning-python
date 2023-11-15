print(
    """If p is the perimeter of a right angle triangle with integral length
sides, {a, b, c}, there are exactly three solutions for p = 120.
    {20,48,52}, {24,45,51}, {30,40,50}
For which value of p <= 1000, is the number of solutions maximised?

expected result: 840
"""
)

res, max = 0, 0
for p in range(5, 1001):
    s = 0
    for c in range(p, p//3, -1):
        for b in range(1, c):
            a = p - c - b
            if (a**2 + b**2) == c**2:
                s+=1
    if s > max:
        max, res = s, p

print("result:", res)

