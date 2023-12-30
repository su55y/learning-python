print(
    """The decimal number, 585 = 1001001001 (binary), is palindromic in both
bases.
Find the sum of all numbers, less than one million, which are palindromic in
base 10 and base 2.
(Please note that the palindromic number, in either base, may not include
leading zeros.)

expected result: 872187
"""
)


def is_palindromic(n: int) -> bool:
    if (d := f"{n}") != d[::-1]:
        return False
    if (b := f"{n:b}") != b[::-1]:
        return False
    return True


print("result:", sum(filter(is_palindromic, range(1_000_000))))
