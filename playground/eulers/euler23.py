print(
    """A perfect number is a number for which the sum of its proper divisors
is exactly equal to the number. For example, the sum of the proper divisors of
28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.
A number n is called deficient if the sum of its proper divisors is less than
n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest
number that can be written as the sum of two abundant numbers is 24.
By mathematical analysis, it can be shown that all integers greater than 28123
can be written as the sum of two abundant numbers. However, this upper limit
cannot be reduced any further by analysis even though it is known that the
greatest number that cannot be expressed as the sum of two abundant numbers is
less than this limit. Find the sum of all the positive integers which cannot be
written as the sum of two abundant numbers.

expected result: 4179871"""
)

# var writable []bool
LIMIT = 28124
writable = [False for _ in range(LIMIT)]
abunList = []
# var limit int
# var abunList *list.List

import math
def divisors_sum(inp: int) -> int:
    limit = int(math.sqrt(inp))
    sum = 0
    for i in range(1, limit+1):
        if inp%i == 0:
            sum += i
        else:
            sum += i + (inp / i)
    return int(sum - inp)

for i in range(1, LIMIT):
    if i < divisors_sum(i):
        abunList.append(i)
# MAIN
# abunList = list.New()
# limit = 28124
# writable = make([]bool, limit)
# for i := 1; i < limit; i++ {
#     writable[i] = false
#     if i < sumOfProperDivisors(i) {
#         abunList.PushBack(i)
#     }
# }

for i, v in enumerate(abunList):
    for j in abunList[i:]:
        if (sum := i + j) < LIMIT:
            writable[sum] = True

# for i := abunList.Front(); i != nil; i = i.Next() {
#     for j := i; j != nil; j = j.Next() {
#         if sum := i.Value.(int) + j.Value.(int); sum < limit {
#             writable[sum] = true
#         }
#     }
# }
# }


sum = 0
for i in range(1, LIMIT):
    if not writable[i]:
        sum += i

# sum := 0
# for i := 1; i < limit; i++ {
#     if !writable[i] {
#         sum += i
#     }
# }
# println(sum)
# ------------ END MAIN
print("result:", sum)