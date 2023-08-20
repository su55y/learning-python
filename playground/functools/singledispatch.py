from collections.abc import Iterable
from functools import singledispatch


@singledispatch
def remove(_, subj):
    raise NotImplemented("cannot remove from %s" % type(subj))


@remove.register(str)
def _(to_remove, subj):
    print("string implementation called")
    return "".join(c for c in subj if not c in to_remove)


@remove.register(dict)
def _(to_remove, subj):
    print("dictionary implementation called")
    return {k: v for k, v in subj.items() if not k in to_remove.keys()}


@remove.register(Iterable)
def _(to_remove, subj):
    print("iterable implementation called")
    return type(subj)(item for item in subj if not item in to_remove)


if __name__ == "__main__":
    assert remove("b", "abc") == "ac"
    assert remove([2], [1, 2, 3]) == [1, 3]
    assert remove({2}, {1, 2, 3}) == {1, 3}
    assert remove((2,), (1, 2, 3)) == (1, 3)
    assert remove({"b": _}, {"a": 1, "b": 2, "c": 3}) == {"a": 1, "c": 3}
