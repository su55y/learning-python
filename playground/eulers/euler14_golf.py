L=1000000
a=[0 for _ in range(L)]
m=r=0
for i in range(1,L):
    j=i
    s=0
    while 1:
        if j==1:
            a[i]=s
            if s>m:m,r=s,i
            break
        elif j<i:
            a[i]=(s:=s+a[j])
            if s>m:m,r=s,i
            break
        j=j*3+1 if j%2 else j//2
        s+=1
print(r)
