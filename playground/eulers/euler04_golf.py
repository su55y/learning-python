r=0
for i in range(100,1000):
    for j in range(i,1000):
        if(s:=str(p:=i*j))==str(s)[::-1] and p>r:
            r=p
print(r)
