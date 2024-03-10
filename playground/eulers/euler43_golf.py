r=0
def f(p,s):
    global r
    if len(s)==0and p[0]!="0"and all(int(p[i+1:i+4])%d==0 for i,d in enumerate((2,3,5,7,11,13,17))):r+=int(p)
    else:
        for i in range(len(s)):f(p+s[i:i+1],s[:i]+s[i+1:])
print(f("","0123456789")or r)
