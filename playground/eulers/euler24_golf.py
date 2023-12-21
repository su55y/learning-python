u=[0for _ in range(10)]
m=999999
r=""
for i in range(9,0,-1):
    p=1
    for j in range(i,0,-1):p*=j
    k,m=divmod(m,p);j=-1
    while(j:=j+1)<k or u[j]:k+=u[j]
    u[j]=1;r+=str(j)
print(r+str(m))
