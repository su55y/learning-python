import math,itertools as i
for a,b in i.combinations_with_replacement(range(1,501),2):
    if (c:= math.sqrt(n:=a*a+b*b))**2==n and a+b+c==1000: print(a*b*c);break
