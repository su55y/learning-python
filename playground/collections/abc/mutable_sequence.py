from collections.abc import Iterable, MutableSequence
from typing import Any, Optional


class List(MutableSequence):
    def __init__(self, __elements: Optional[Iterable] = None, /) -> None:
        self.__elements = list(__elements) if __elements else list()

    def insert(self, index: int, value: Any) -> None:
        self.__elements.insert(index, value)

    def __setitem__(self, index: int, value: Any) -> None:
        self.__elements[index] = value

    def __getitem__(self, index: int) -> Any:
        return self.__elements[index]

    def __delitem__(self, index: int) -> None:
        del self.__elements[index]

    def __len__(self):
        return len(self.__elements)

    def __repr__(self):
        return "Array(%s)" % self.__elements

    def __str__(self):
        return "[%s]" % ", ".join(str(e) for e in self.__elements)
