with open("input08.txt") as f:
    n=f.read()
import functools as f
r=0
for i in range(len(n)-5):
    if (p:=f.reduce(lambda p,j:p*int(n[j]),range(i,i+5),1))>r:
        r=p
print(r)
