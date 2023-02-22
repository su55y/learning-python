from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Database:
    host: str
    port: str
    name: str
    tables: List[str]


@dataclass
class Server:
    host: str
    port: str
    url: str | None = None


@dataclass
class Servers:
    prod: Server
    test: Dict[str, Server]
