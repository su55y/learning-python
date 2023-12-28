def f(n,m,c=[1,2,5,10,20,50,100,200]):
    if n==0:return 1
    if n<0 or(n>0and m<1):return 0
    return f(n,m-1)+f(n-c[m-1],m)
print(f(200,8))
