with open("input11.txt") as f:l=f.read().strip().split("\n",20)
arr=[[int(s)for s in l[i].split()]for i in range(20)]
res=max([arr[i][j]*arr[i][j+1]*arr[i][j+2]*arr[i][j+3]for i in range(20)for j in range(17)])
res=m if(m:=max([arr[i][j]*arr[i+1][j]*arr[i+2][j]*arr[i+3][j]for i in range(17)for j in range(20)]))>res else res
res=m if(m:=max([arr[i][j]*arr[i+1][j+1]*arr[i+2][j+2]*arr[i+3][j+3]for i in range(17)for j in range(17)]))>res else res
res=m if(m:=max([arr[i][j]*arr[i-1][j+1]*arr[i-2][j+2]*arr[i-3][j+3]for i in range(3,20)for j in range(17)]))>res else res
print(res)
