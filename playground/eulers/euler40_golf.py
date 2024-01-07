c,l,r=0,10,1
i=0
while l<1000001:
    if(c:=c+len(s:=str(i:=i+1)))>=l:r*=int(s[len(s)-(c-l)-1:len(s)-(c-l)]);l*=10
print(r)
