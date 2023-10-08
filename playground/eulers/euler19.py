print(
    """You are given the following information, but you may prefer to do some research for yourself.

  * 1 Jan 1900 was a Monday.
  * Thirty days has September,
  * April, June and November.
  * All the rest have thirty-one,
  * Saving February alone,
  * Which has twenty-eight, rain or shine.
  * And on leap years, twenty-nine.
  * A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

expected result: 171
"""
)

days_in_months = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30]
months = [0 for _ in range(12)]
for i in range(11):
    months[i + 1] = (months[i] + days_in_months[i]) % 7

sundays = 0
for y in range(1900, 2000):
    for i in range(len(months)):
        c = 366 if (y % 4 == 0 and i <= 1) or ((y + 1) % 4 == 0 and i > 1) else 365
        if (d := (months[i] + c) % 7) == 6:
            sundays += 1
        months[i] = d

print("result:", sundays)
