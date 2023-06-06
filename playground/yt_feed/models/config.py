from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Channel:
    title: str = ""
    channel_id: str = ""


@dataclass
class Config:
    channels: List[Channel]
    log_file: Optional[Path] = None
    log_stdout: bool = False
