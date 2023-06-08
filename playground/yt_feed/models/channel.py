from dataclasses import dataclass, field
from typing import List

from models.entry import Entry


@dataclass
class Channel:
    title: str = ""
    channel_id: str = ""
    entries: List[Entry] = field(default_factory=list)
