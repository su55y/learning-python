from .entities import Database, Servers
from dataclasses import dataclass


@dataclass(eq=True)
class Config:
    database: Database
    servers: Servers
