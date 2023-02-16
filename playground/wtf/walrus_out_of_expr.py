(val := "some value")
print(val)

xy = "foo", "bar"
print("xy:", xy)

x, y = xy

(xy2 := x, y)
print("xy2:", xy2)

(xy2, y2 := y, y)
print("xy2, y2:", (xy2, y2))
