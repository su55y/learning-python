print(
    """Take the number 192 and multiply it by each of 1, 2, and 3:
    192 * 1 = 192
    192 * 2 = 384
    192 * 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576. We will
call 192384576 the concatenated product of 192 and (1,2,3). The same can be
achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the
pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).
What is the largest 1 to 9 pandigital 9-digit number that can be formed as the
concatenated product of an integer with (1,2,...,n) where n > 1?

expected result: 932718654 
"""
)

def is_pandigital(s: str) -> bool:
    for n in range(1, 10):
        if str(n) not in s:
            return False
    return True

res = 0
for i in range(1, 10_000):
    s = ""
    for j in range(1, 9):
        s = "%s%d" % (s, i*j)
        if len(s) >= 9:
            break
    if len(s) == 9 and is_pandigital(s) and (n := int(s)) > res:
        res = n
print("result:", res)
