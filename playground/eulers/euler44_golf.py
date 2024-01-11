a=[(i*(3*i-1))//2for i in range(2500)]
def f(v,l,h):
    if h<l:return 0
    if a[m:=l+(h-l)//2]>v:return f(v,l,m-1)
    elif a[m]<v:return f(v,m+1,h)
    return 1
print(min(a[j]-a[i]for i,j in __import__("itertools").combinations(range(1,2500),2)if f(a[j]-a[i],0,2499)and f(a[j]+a[i],0,2499)))
