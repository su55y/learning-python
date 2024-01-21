import itertools as t
c={0:0,1:1}
L=4000000
def f(n):
    if n in c:return c[n]
    c[n]=f(n-1)+f(n-2)
    return c[n]
print(sum(n for n in(c[i]for i in t.takewhile(lambda x:f(x)<L,t.count()))if n%2==0))
