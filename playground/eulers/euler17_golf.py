def f(n):
    if (r:={0:0,1:3,2:3,6:3,10:3,4:4,5:4,9:4,3:5,7:5,8:5,40:5,50:5,60:5,11:6,12:6,20:6,30:6,80:6,90:6,15:7,16:7,70:7,13:8,14:8,18:8,19:8,17:9,1000:11}.get(n)) is not None:return r
    if n<100:return f(n-(n%10))+f(n%10)
    if n%100==0:return f(n//100)+7
    return f(n//100)+10+f(n % 100)
print(sum(f(i) for i in range(1001)))