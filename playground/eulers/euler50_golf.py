LIMIT=1000000
a=[1,1,*[0for _ in range(LIMIT-2)]]
p=3
while 1:
    for i in range(2*p,LIMIT,p):a[i]=1
    i=p+2
    while i<LIMIT and a[i]:i+=2
    if i<LIMIT:p=i
    else:break
p=[2,*[i for i in range(LIMIT)if a[i]==0and i%2]]
r,m=0,0
for i in range(l:=len(p)):
    t,c=p[i],0
    for j in range(i+1,l):
        t+=p[j]
        c+=1
        if t>(LIMIT-1):break
        if t%2 and not a[t] and c>m:m=c;r=t
print(r)
