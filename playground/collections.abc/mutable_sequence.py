from collections.abc import Iterable, MutableSequence
from typing import Any, Optional


class Array(MutableSequence):
    def __init__(self, __size: Optional[int], /) -> None:
        self.__elements = list(None for _ in range(__size)) if __size else list()

    def insert(self, index: int, value: Any) -> None:
        self.__elements.insert(index, value)

    def fill(self, elements: Iterable) -> "Array":
        i = 0
        for e in elements:
            self.__elements[i] = e
            i += 1
            if i >= len(self.__elements):
                break
        return self

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


if __name__ == "__main__":
    print(Array(3).fill([1, 2, 3, 4]))
    print(Array(5).fill([1, 2, 3, 4]))
