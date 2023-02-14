from pkg1.subpkg1 import mod2
from .mod3 import Mod3Class


def mod4method():
    return Mod3Class(mod2.mod2method())
