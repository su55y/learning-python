f=[1,*[0for _ in range(9)]]
for i in range(1,10):f[i]=f[i-1]*i
t=10
l=f[-1]
while l>t:l*=2;t*=10
s=0
for i in range(10,l):
    n,j=0,i
    while j>9:n+=f[j%10];j//=10
    n+=f[j]
    if i==n:s+=i
print(s)
