from functools import reduce
print(
    """The nth term of the sequence of triangle numbers is given by,
t{n} = frac12n(n+1); so the first ten triangle numbers are:
    1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
By converting each letter in a word to a number corresponding to its
alphabetical position and adding these values we form a word value. For example,
the word value for SKY is 19 + 11 + 25 = 55 = t{10}. If the word value is a
triangle number then we shall call the word a triangle word.
Using [words.txt](https://projecteuler.net/resources/documents/0042_words.txt),
a 16K text file containing nearly two-thousand common English words, how many
are triangle words?

expected result: 162
"""
)


inp = ""
with open("input42.txt") as f:
    inp = f.read().split(",")
triangles = [(i*(i+1))//2 for i in range(20)]
print("result:", reduce(lambda p, n: p+1 if sum(ord(ch)-ord('A')+1 for ch in n) in triangles else p, [w.split('"')[1] for w in inp], 0))
