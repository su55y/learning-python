from dataclasses import dataclass
from typing import List


@dataclass
class Channel:
    title: str = ""
    channel_id: str = ""
    url: str = ""


@dataclass
class Config:
    channels: List[Channel]
