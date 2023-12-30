def f(a,b,n):
    if len(s:=f"{a}{b}{n}")!=9:return 0
    for i in range(1, 10):
        if not(f"{i}"in s):return 0
    return n
print(sum({f(i,j,i*j)for i in range(1,200)for j in range(1,5000)}))
