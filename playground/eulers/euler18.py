print(
    """By starting at the top of the triangle below and moving to adjacent numbers
on the row below, the maximum total from top to bottom is 23.

       3
      7 4
     2 4 6
    8 5 9 3

That is, 3 + 7 + 4 + 9 = 23. Find the maximum total from top to bottom of the triangle below:

75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

NOTE: As there are only 16384 routes, it is possible to solve this problem by
trying every route. However, Problem 67, is the same challenge with a triangle
containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)

expected result: 1074
"""
)

inp = ""
with open("input18.txt") as f:
    inp = f.read().strip().split("\n")

arr = [[int(s) for s in inp[i].split()] for i in range(len(inp))]
bests = [[-1 for _ in range(len(arr[i]))] for i in range(len(arr))]


def best_sum(i: int, j: int) -> int:
    global arr, bests
    if i == len(arr) - 1:
        return arr[i][j]

    bests[i][j] = bests[i][j] if bests[i][j] != -1 else (arr[i][j] + l if (l := best_sum(i + 1, j)) > (r := best_sum(i + 1, j + 1)) else arr[i][j] + r)
    return bests[i][j]


print("result:", best_sum(0, 0))
