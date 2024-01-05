r=0
for i in range(1,10000):
    s=""
    for j in range(1,9):
        if len(s:=f"{s}{i*j}")>8:break
    if 9==len(s)and all(str(c)in s for c in range(1,10))and(n:=int(s))>r:r=n
print(r)
