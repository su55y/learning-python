import itertools as t
import math as m
i=r=0
c=t.count(2)
while i<10001:
    p=1
    for j in range(2,m.floor((r:=next(c))**0.5)+1):
        if r%j==0: p=0;break
    if p: i+=1
print(r)
