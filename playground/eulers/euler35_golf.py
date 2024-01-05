L=1000000
a=[0,1,*[0for _ in range(L)]]
p=3
r=13
c=0
while 1:
    for i in range(p*2,L,p):a[i]=1
    i=p+2
    while i<L and a[i]:i+=2
    if i<L:
        if(p:=i)<101:continue
        b=0
        c=1
        for i in range(len(s:=str(p))-1):
            if (t:=int(s:=s[1:]+s[0]))>p:b=1;break
            elif a[t]==0and t%2!=0:c+=1
            else:b=1;break
        if b==0:r+=c
    else:
        break
print(r)
