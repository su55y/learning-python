a=[[0for _ in range(21)]for _ in range(21)]
a[20][20]=1
def f(i,j):
    if a[i][j]:return a[i][j]
    if i<20and j<20:a[i][j]=f(i+1,j)+f(i,j+1)
    elif i<20and j==20:a[i][j]=f(i+1,j)
    else:a[i][j]=f(i,j+1)
    return a[i][j]
print(f(0,0))
