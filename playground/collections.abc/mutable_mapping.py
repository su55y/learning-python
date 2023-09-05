from collections.abc import Hashable, Iterable, MutableMapping
from typing import Any, Optional, Tuple, Union

Items = Union[MutableMapping[Hashable, Any], Iterable[Tuple[Hashable, Any]]]


class Map(MutableMapping):
    def __init__(self, __items: Optional[Items] = None, /, **kwargs) -> None:
        self.__items = {}
        if __items is not None:
            self.update(dict(__items))
        self.update(dict(kwargs))

    def __getitem__(self, key):
        return self.__items[key]

    def __setitem__(self, key, value):
        self.__items[key] = value

    def __delitem__(self, key):
        del self.__items[key]

    def __iter__(self):
        return iter(self.__items)

    def __len__(self):
        return len(self.__items)

    def __repr__(self):
        return repr(self.__items)
