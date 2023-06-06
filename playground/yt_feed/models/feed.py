from dataclasses import dataclass
from typing import List

from models.entry import Entry


@dataclass
class Feed:
    channel_id: str
    title: str
    is_active: bool
    entries: List[Entry]
