print(
    """
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit number
s is 9009 = 91 × 99.
Find the largest palindrome made from the product of two 3-digit numbers.

expected result: 906609
"""
)


def result() -> int:
    i = j = i_stop = j_stop = 1000
    while (i := i - 1) > 100:
        while (j := j - 1) > 100:
            if str(r := i * j) == str(r)[::-1]:
                return r
            if j % 10 == 0:
                break

        j = j_stop = i_stop if i_stop % 10 == 0 else j_stop - 10

    return 0


print("result:", result())
