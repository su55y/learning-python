L=1000000
a=[1,1,*[0for _ in range(L-2)]]
c,r=2,3
while(t:=1):
    for i in range(2*r,L,r):a[i]=1
    i=r+2
    while i<L and a[i]:i+=2
    if i<L:r=i;c+=1
    else:break
p=[2,*[0for _ in range(c-1)]]
for i in range(3,L,2):
    if a[i]==0:p[t]=i;t+=1
for i in range(646,L):
    y=0
    for j in range(i,i+4):
        if a[j]==(x:=0)and j%2:break
        for k in range(c):
            if(a[j]==0and j%2)or(j%p[k]==0):
                if(x:=x+1)==4:
                    if(y:=y+1)==4:print(i);exit(0)
                    break
                elif a[j]==0and j%2:break
                while j%p[k]==0:j//=p[k]
