from pkg1.subpkg2 import mod4


def mod5method():
    return f"{mod4.mod4method()} in {__name__}.{mod5method.__name__}"
