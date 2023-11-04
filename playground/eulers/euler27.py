print(
    """Euler discovered the remarkable quadratic formula:
    n^2 + n + 41
It turns out that the formula will produce 40 primes for the consecutive
integer values 0 <= n <= 39. However, when n = 40, 40^2 + 40 + 41 = 40(40 + 1)
+ 41 is divisible by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly
divisible by 41.
The incredible formula n^2 - 79n + 1601 was discovered, which produces 80
primes for the consecutive values 0 <= n <= 79. The product of the
coefficients, -79 and 1601, is -126479.
Considering quadratics of the form:

    n^2 + an + b, where |a| < 1000 and |b| <= 1000

    where |n| is the modulus/absolute value of n
    e.g. |11| = 11 and |-4| = 4

Find the product of the coefficients, a and b, for the quadratic expression
that produces the maximum number of primes for consecutive values of n,
starting with n = 0.

expected result: """
)
import math

# func isPrime(in int) bool {
# limit := int(math.Sqrt(float64(in)))
# if in < 2 || in%2 == 0 {
#     return false
# } else {
#     for i := 2; i < limit; i++ {
#         if in%i == 0 {
#             return false
#         }
#     }
# }
# return true
# }

from functools import cache

@cache
def is_prime(n: int) -> bool:
    print(n)
    if n < 2 or n % 2 == 0:
        return False
    for i in range(2, int(math.sqrt(n))):
        if n % i == 0:
            return False
    return True

counter = 0
am, bm = 0, 0
for a in range(-999, 1000):
    for b in range(-999, 1000):
        print(counter)
        n = 0
        while not is_prime(n*n + a*n + b):
            if n > counter:
                counter, am, bm = n, a, b
            n += 1
# var maxCounter, aInMax, bInMax int
# maxCounter = 0
# FIXME: findout how break works !!!!!!!!!
# for a := -999; a < 1000; a++ {
#     for b := -999; b < 1000; b++ {
#     inner:
#         for n := 0; ; n++ {
#             if !isPrime(n*n + a*n + b) {
#                 if n > maxCounter {
#                     maxCounter, aInMax, bInMax = n, a, b
#                 }
#                 break inner

# println(aInMax * bInMax)
# --- END OF MAIN
print("result:", am+bm)
