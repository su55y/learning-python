from dataclasses import dataclass
from typing import Dict


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
    url: str | None = None


@dataclass
class Servers:
    prod: Server
    test: Dict[str, Server]
