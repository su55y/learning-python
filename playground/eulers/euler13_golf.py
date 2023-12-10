import functools as t
with open("input13.txt") as f:N=f.read()
l=N.split("\n",99)
r=""
m=0
for i in range(49,-1,-1):
    m,d=divmod(t.reduce(lambda p,n:p+int(l[n][i]),range(100),m),10)
    r=str(d)+r
print(f"{m}{r}"[:10])
