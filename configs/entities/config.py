from .entities import Database, Servers
from dataclasses import dataclass
from typing import Dict


@dataclass
class Config:
    database: Database
    servers: Servers
