from collections.abc import Hashable, Iterable, MutableSet
from typing import Optional


class Set(MutableSet):
    def __init__(self, __iterable: Optional[Iterable[Hashable]] = None, /):
        self.__elements = set(__iterable) if __iterable else set()

    def __contains__(self, value):
        return value in self.__elements

    def __iter__(self):
        return iter(self.__elements)

    def __len__(self):
        return len(self.__elements)

    def add(self, value):
        self.__elements.add(value)

    def discard(self, value):
        self.__elements.discard(value)

    def __repr__(self):
        return "Set(%s)" % self.__elements

    def __str__(self):
        return "[%s]" % ", ".join(str(e) for e in self.__elements)
