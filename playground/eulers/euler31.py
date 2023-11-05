from functools import cache

print(
    """In the United Kingdom the currency is made up of pound (£) and pence (p).
There are eight coins in general circulation:
    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
It is possible to make £2 in the following way:
    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?


expected result: 73682
"""
)

coins = [1, 2, 5, 10, 20, 50, 100, 200]

@cache
def calc(n, m):
    global coins
    if n == 0:
        return 1
    elif n < 0 or (n >= 1 and m <= 0):
        return 0
    return calc(n, m-1) + calc(n-coins[m-1], m)


print("result:", calc(200, len(coins)))
