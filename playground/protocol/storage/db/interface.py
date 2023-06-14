from typing import List, Protocol, Tuple

Rows = List[Tuple[str, ...]]


class IDataBase(Protocol):
    def select(self, query: str) -> Rows:
        ...

    def insert(self, query: str, rows: Rows) -> int:
        ...

    def delete(self, query: str) -> int:
        ...
