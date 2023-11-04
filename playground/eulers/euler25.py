print(
    """HUH
    A permutation is an ordered arrangement of objects. For example, 3124 is
one possible permutation of the digits 1, 2, 3 and 4. If all of the
permutations are listed numerically or alphabetically, we call it lexicographic
order. The lexicographic permutations of 0, 1 and 2 are:
    012 021 102 120 201 210
What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5,
6, 7, 8 and 9?

expected result: 4782"""
)

a, b, c, counter = 1, 2, 0, 2

while len(str(a)) < 1000:
    # print(f"{a=}, {b=}, {c=}")
    # c -= abs(a)
    c = c -a
    a += b
    # b -= abs(c)
    b = b -c

    counter+=1
print("result:", counter)
print(str(a))

# FIXME: test big.Int stuff !!!!!
# a, b, c, counter := big.NewInt(int64(1)), big.NewInt(int64(2)), big.NewInt(int64(0)), 2
# for len(a.String()) < 1000 {
#     c.Neg(a) //c is a temp variable
#     a.Add(a, b)
#     b.Neg(c)
#     counter++
# }
# println(counter)
