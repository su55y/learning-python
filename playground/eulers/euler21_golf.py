import math,functools as f
def s(n):
    r=0
    for i in range(1,int(math.sqrt(abs(n)))+1):
        if n%i==0:r=r+i if i==n//i else r+i+(n//i) 
    return r-n
print(f.reduce(lambda p,n:p+n if n==s(j:=s(n))and n!=j else p,range(1,10000)))
