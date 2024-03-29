print(
    """The number, 1406357289, is a 0 to 9 pandigital number because it is made
up of each of the digits 0 to 9 in some order, but it also has a rather
interesting sub-string divisibility property.
Let d{1} be the 1st digit, d{2} be the 2nd digit, and so on. In this way, we
note the following:
    d{2}*d{3}*d{4}=406 is divisible by 2
    d{3}*d{4}*d{5}=063 is divisible by 3
    d{4}*d{5}*d{6}=635 is divisible by 5
    d{5}*d{6}*d{7}=357 is divisible by 7
    d{6}*d{7}*d{8}=572 is divisible by 11
    d{7}*d{8}*d{9}=728 is divisible by 13
    d{8}*d{9}*d{10}=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.

expected result: 16695334890
"""
)

res = 0


def check_prop(s: str):
    if s.startswith("0"):
        return
    for i in range(1, 8):
        if int(s[i : i + 3]) % (2, 3, 5, 7, 11, 13, 17)[i - 1] != 0:
            return
    global res
    res += int(s)


def all_perms(pre: str, s: str):
    if len(s) == 0:
        check_prop(pre)
    else:
        for i in range(len(s)):
            all_perms(pre + s[i : i + 1], s[:i] + s[i + 1 :])


all_perms("", "0123456789")
print("result:", res)
