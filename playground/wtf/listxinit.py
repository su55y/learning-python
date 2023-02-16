l1 = [0] * 3
l2 = [l1] * 3
print("l2:", l2)

l2[0][0] = 1
print("l2:", l2)

l3 = [[0] * 3 for _ in range(3)]
print("l3:", l3)
l3[0][0] = 1
print("l3:", l3)
