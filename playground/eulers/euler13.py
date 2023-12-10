NUMBER = ...
with open("./input13.txt") as f:
    NUMBER = f.read()

if len(NUMBER) != 5100:
    exit("invalid input")

print(
    """Work out the first ten digits of the sum of the following one-hundred
50-digit numbers.
%s...

expected result: 5537376230
"""
    % NUMBER[: len(NUMBER) // 6]
)

lines = NUMBER.split("\n", 99)

res = ""
reminder = 0
for i in range(49, -1, -1):
    sum = reminder
    for j in range(len(lines)):
        sum += int(lines[j][i])
    reminder, digit = divmod(sum, 10)
    res = "%s%s" % (digit, res)

res = ("%s%s" % (reminder, res))[:10]
print("result:", res)
