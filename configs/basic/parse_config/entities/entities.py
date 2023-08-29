from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Database:
    host: str
    port: str
    name: str
    tables: list[str]


@dataclass
class Server:
    host: str
    port: str
    url: Optional[str] = None


@dataclass
class Servers:
    prod: Server
    test: Dict[str, Server]
