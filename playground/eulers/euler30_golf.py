def f(n):
    s=0
    while n:n,r=divmod(n,10);s+=r**5
    return s
print(sum(i for i in range(22,9**5*4)if i==f(i)))
