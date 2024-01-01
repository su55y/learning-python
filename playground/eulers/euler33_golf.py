r=1
for i in range(1,10):
    for j in range(1,i):
        for k in range(1,j):r*=b/a if(a:=10*k+i)*j==(b:=10*i+j)*k else 1
print(int(r))
