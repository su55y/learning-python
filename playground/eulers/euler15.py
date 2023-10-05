print(
    """Starting in the top left corner of a 2*2 grid, and only being able to move to the right and down,
there are exactly 6 routes to the bottom right corner. (https://projecteuler.net/resources/images/0015.png?1678992052)
How many such routes are there through a 20*20 grid?

expected result: 137846528820
"""
)

arr = [[0 for _ in range(21)] for _ in range(21)]
arr[20][20] = 1


def routes_count(i: int, j: int) -> int:
    global arr
    if arr[i][j] != 0:
        return arr[i][j]
    res = 0
    if i < 20 and j < 20:
        res = routes_count(i + 1, j) + routes_count(i, j + 1)
    elif i < 20 and j == 20:
        res = routes_count(i + 1, j)
    else:
        res = routes_count(i, j + 1)
    arr[i][j] = res
    return res


print("result:", routes_count(0, 0))
