k1 = 1
k2 = 1.0
k3 = 1 + 0j
print(type(k1), type(k2), type(k3))
print(k1 == k2 == k3)

d1 = {}
for i, k in enumerate([k1, k2, k3]):
    d1[k] = i + 1
    print("d1:", d1)
