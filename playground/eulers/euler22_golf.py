with open("input22.txt")as f:(inp:=[n.split('"',-1)[1]for n in f.read().strip().split(",",-1)]).sort()
import functools as t
print(sum(int(i+1)*t.reduce(lambda p,n:p+(ord(n)-64),n,0)for i,n in enumerate(inp)))
