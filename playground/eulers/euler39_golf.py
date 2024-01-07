r,m=0,0
for p in range(5,1001):
    s=0
    for c in range(p,p//3,-1):
        for b in range(1,c):s+=((a:=p-c-b)*a+b*b)==c*c
    if s>m:m,r=s,p
print(r)
