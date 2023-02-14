from .mod1 import mod1method


def mod2method():
    return f"{mod1method()} in {__name__}.{mod2method.__name__}"
