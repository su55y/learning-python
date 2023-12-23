i,p,L=0,3,1000
l=[1,1,*[0for _ in range(L-2)]]
while 1:
    for i in range(p*2,L,p):l[i]=1
    i=p+2
    while i<L and l[i]:i+=2
    if i>=L:break
    p=i
for i in range(p,0,-2):
    if l[i]==0 and i%2:
        for j in range(1,i):
            if((10**j)-1)%i==0:break
        if i-j==1:print(i);exit(0)
