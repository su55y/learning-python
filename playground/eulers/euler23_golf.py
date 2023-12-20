import math
def s(n):
    r=0
    for i in range(1,int(math.sqrt(abs(n)))+1):
        if n%i==0:r=r+i if i==n//i else r+i+(n//i) 
    return r-n
r=set(range(L:=28124))
for i,a in enumerate(l:=[i for i in range(1,L)if i<s(i)]):
    for b in l[i:]:
        if(j:=a+b)<L:r.discard(j)
print(sum(r))
