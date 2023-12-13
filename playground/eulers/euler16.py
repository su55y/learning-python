print(
    """2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.
What is the sum of the digits of the number 2^1000?

expected result: 1366
"""
)


def multiply(s: str) -> str:
    res, reminder = "", 0
    for i in range(len(s) - 1, -1, -1):
        n = int(s[i]) * 2 + reminder
        reminder, n = divmod(n, 10)
        res = "%s%s" % (n, res)
    if reminder > 0:
        return "%s%s" % (reminder, res)
    return res


s = "2"
for i in range(999):
    s = multiply(s)
res = 0
for i in range(len(s)):
    res += int(s[i])
print("result:", res)
