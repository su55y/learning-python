import itertools as t
import math
def f(n):
    if n<2 or n%2==0:return 1
    for i in range(2,int(math.sqrt(n)//1)):
        if n%i==0:return 1
am,bm,c=0,0,0
for a,b in t.product(range(-999,1000),repeat=2):
    for n in t.count():
        if f(n*n+a*n+b):
            if n>c:c,am,bm=n,a,b
            break
print(am*bm)
