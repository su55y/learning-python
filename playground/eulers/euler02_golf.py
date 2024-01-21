import itertools as t
c={0:0,1:1}
L=4000000
def f(n):
    if n in c:
        return c[n]
    c[n]=f(n-1)+f(n-2)
    return c[n]
print(__import__('functools').reduce(lambda p,n:p+n if n%2==0 else p,[c[i] for i in t.takewhile(lambda x:f(x)<L,t.count())]))
