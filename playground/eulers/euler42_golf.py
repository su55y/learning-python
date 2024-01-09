with open("input42.txt")as f:s=f.read().split(",")
print(sum(int(sum(ord(c)-ord("A")+1for c in w.split('"')[1])in{(i*(i+1))//2for i in range(20)})for w in s))
