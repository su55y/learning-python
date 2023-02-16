import uuid

hex = lambda: uuid.uuid4().hex[:4]


def foo(some_list=[]):
    some_list.append(0)
    return some_list


print(foo())
print(foo())
print(foo([1]))
print(foo())


def bar(some_dict={}):
    some_dict[hex()] = 0
    return some_dict


print(bar())
print(bar())
print(bar({"*NEW*": 1}))
print(bar())
