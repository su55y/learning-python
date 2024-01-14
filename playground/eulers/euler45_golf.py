a=[i*(3*i-1)//2for i in range(80000)]
def f(v,l=1,h=79999):
    if h<l:return 1
    global a
    if a[m:=l+(h-l)//2]>v:return f(v,l,m-1)
    elif a[m]<v:return f(v,m+1,h)
i=143
while 1:
    if not f(r:=(i:=i+1)*(2*i-1)):print(r);break
