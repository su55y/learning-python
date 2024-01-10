r=0
def f(p,s):
    global r
    if not len(s):
        if p[0]=="0":return
        for i in range(1,8):
            if int(p[i:i+3])%[2,3,5,7,11,13,17][i-1]:return
        r+=int(p)
    else:
        for i in range(len(s)):f(p+s[i:i+1],s[:i]+s[i+1:])
print(f("","0123456789")or r)
