L=87654322
a=[1,1,*[0 for _ in range(L-2)]]
p=3
while 1:
    for i in range(2*p,L,p):a[i]=1
    i=p+2
    while i<L and a[i]:i+=2
    if i<L:p=i
    else:break

for i in range(L-1,0,-2):
    s=str(i)
    if not a[i] and all(str(n) in s for n in range(1,len(s)+1)):print(i);break
