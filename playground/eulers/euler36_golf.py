print(sum(i for i in range(10**6)if(d:=str(i))==d[::-1]and(b:=f"{i:b}")==b[::-1]))
