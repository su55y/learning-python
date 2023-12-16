with open("input18.txt")as f:f=f.read().strip().split("\n")
L=len(a:=[[int(s)for s in f[i].split()]for i in range(len(f))])
b=[[-1 for _ in range(len(a[i]))] for i in range(L)]
def s(i,j):
    if i==L-1:return a[i][j]
    b[i][j]=b[i][j]if b[i][j]!=-1 else(a[i][j]+l if(l:=s(i+1,j))>(r:=s(i+1,j+1))else a[i][j]+r)
    return b[i][j]
print(s(0,0))
