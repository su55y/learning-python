L=1000000
l,r=(a:=[0for _ in range(L)])[:],a[:]
a[0]=a[1]=a[6]=a[9]=1
for i in [2,3,5,7]:l[i]=r[i]=1
for x in [3,5,7]:
    for i in range(x*2,L,x):a[i]=1
c=s=0
p=11
while 1:
    r[p]=r[p//10]
    if l[int(f"{p}"[1:])]:
        l[p]=1
        if r[p]:
            s+=p
            if(c:=c+1)==11:print(s);exit(0)
    for i in range(p*2,L,p):a[i]=1
    i=p+2
    while i<L and a[i]:i+=2
    if i<L:p=i
    else:exit(1)
