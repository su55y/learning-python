def f(x,y):
    s2=str(y)
    for i in range(len(s1:=str(x))):
        if s2.find(s1[i:i+1])<0 or s1.find(s2[i:i+1])<0:return 0
    return 1
L=10000
a=[0for _ in range(L)]
p=2
while 1:
    for i in range(2*p,L,p):a[i]=1
    i=p+1
    while i<L and a[i]:i+=1
    if i<L:p=i
    else:break
for i in range(1000,L):
    for j in range(i+1,L):
        if i!=1487and f(i,x:=2*j-i)*f(i,j)>0and x<L and a[x]+a[i]+a[j]==0:print(f"{i}{j}{x}");exit(0)
