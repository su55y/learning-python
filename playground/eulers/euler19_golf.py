m=[0for _ in range(12)]
for i in range(11):m[i+1]=(m[i]+[31,29,31,30,31,30,31,31,30,31,30][i])%7
r=0
for y in range(1900, 2000):
    for i in range(len(m)):
        if (d:=(m[i]+(c:=366if(y%4==0and i<=1)or((y+1)%4==0and i>1)else 365))%7)==6:r+=1
        m[i]=d
print(r)
