import itertools as t
import functools as f
import math
r=1
i=t.count(2)
while f.reduce(lambda p,n: p if r%n else p+2,range(1,int(math.sqrt(r))+1),0)<500: r+=next(i)
print(r)
