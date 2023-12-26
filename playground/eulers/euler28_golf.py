r,a,skip=1,1,0
for i in range(2000):r+=(a:=a+(skip:=skip+2if i%4==0 else skip))
print(r)
