r=1
for i in [n for n in range(2,20) if not any(n%i==0 for i in range(2,n))]:
    d=i
    while d<=20: d*=i
    r*=d//i
print(r)
