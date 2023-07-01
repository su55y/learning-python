from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Database:
    host: str
    port: str
    name: str
    tables: List[str]


@dataclass
class Server:
    name: str
    host: str
    port: str
    url: Optional[str] = None
