from dataclasses import dataclass


@dataclass
class Entry:
    id: str
    title: str
    updated: str
    is_viewed: bool = False
