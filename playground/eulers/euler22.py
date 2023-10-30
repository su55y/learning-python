from functools import reduce

print(
    """Using [namex.txt](https://projecteuler.net/resources/documents/0022_names.txt),
a 46K text file containing over five-thousand first names, begin by sorting it
into alphabetical order. Then working out the alphabetical value for each name,
multiply this value by its alphabetical position in the list to obtain a name
score. For example, when the list is sorted into alphabetical order, COLIN,
which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So,
COLIN would obtain a score of 938 * 53 = 49714.
What is the total of all the name scores in the file?

expected result: 871198282"""
)


alphabetic_index = lambda s: reduce(lambda p, n: p + (ord(n) - 64), s, 0)

inp = ""
with open("input22.txt") as f:
    inp = f.read().strip().split(",", -1)

for i, name in enumerate(inp):
    inp[i] = name.split("\"", -1)[1]
inp.sort()

res = 0
for i, name in enumerate(inp):
    res += int(i+1) * alphabetic_index(name)
print("result:", res)
