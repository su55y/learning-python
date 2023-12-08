L=2000000
a=[1,1,*[0 for _ in range(L-2)]]
r,p=5,3
while 1:
    for i in range(p*2,L,p): a[i]=1
    i=p+2
    while i<L and a[i]: i+=2
    if i<L: p=i; r+=i
    else: break
print(r)
