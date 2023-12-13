def f(s):
    r,p=0,""
    for i in range(len(s)-1,-1,-1):r,n=divmod((n:=int(s[i])*2+r),10);p=f"{n}{p}"
    return f"{r}{p}" if r else p
from functools import reduce as r
print(r(lambda p,n:p+int(n),r(lambda p,_:f(p),range(999),"2"),0))
