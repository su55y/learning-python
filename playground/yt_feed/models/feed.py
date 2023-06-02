from dataclasses import dataclass


@dataclass
class Feed:
    channel_id: str
    title: str
