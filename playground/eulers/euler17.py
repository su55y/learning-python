from functools import reduce

print(
    """If the numbers 1 to 5 are written out in words: one, two, three, four,
five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total. If all the
numbers from 1 to 1000 (one thousand) inclusive were written out in words,
how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and
forty-two) contains 23 letters and 115 (one hundred and fifteen) contains
20 letters. The use of "and" when writing out numbers is in compliance with
British usage.

expected result: 21124
"""
)


def numb_len(n: int):
    match n:
        case 0:
            return 0
        case 1 | 2 | 6 | 10:
            return 3  # one, two, six, ten
        case 4 | 5 | 9:
            return 4  # four, five, nine
        case 3 | 7 | 8 | 40 | 50 | 60:
            return 5  # three, seven, eight, forty, fifty, sixty
        case 11 | 12 | 20 | 30 | 80 | 90:
            return 6  # eleven, twelve, twenty, thirty, eighty, ninety
        case 15 | 16 | 70:
            return 7  # fifteen, sixteen, seventy
        case 13 | 14 | 18 | 19:
            return 8  # thirteen, fourteen, eighteen, nineteen
        case 17:
            return 9  # seventeen

    if n < 100:
        return numb_len(n - (n % 10)) + numb_len(n % 10)
    if n % 100 == 0:
        return numb_len(n // 100) + 7
    return numb_len(n // 100) + 10 + numb_len(n % 100)


print("result:", reduce(lambda p, n: p + numb_len(n), range(1000), len("onethousand")))
