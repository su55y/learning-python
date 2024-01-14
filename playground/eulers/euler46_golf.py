import math
a=[0,0,1,*[0for _ in range(999997)]]
for i in __import__('itertools').count(3,2):
    t=0
    for j in range(2,i):
        if a[j] and i%j==0and(t:=1):break
    if t:
        for j in range(2,i):
            if a[j]:
                if(n:=i-j)%2==0and int(math.sqrt(int(n/2)))**2==n//2:break
        else:print(i);exit(0)
    else:a[i]=1
