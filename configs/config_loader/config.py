from dataclasses import dataclass, field
import json
from pathlib import Path
import toml
from typing import Dict, List, Optional

import yaml

from entities import Database, Server


@dataclass(eq=True)
class Config:
    database: Optional[Database] = None
    servers: List[Server] = field(default_factory=list)

    def __init__(self, path: Optional[Path] = None, **kwargs) -> None:
        if path:
            if not path.exists():
                raise Exception("%s not found" % path)
            if _dict := self._read(path):
                self._parse(_dict)
        else:
            self.database = kwargs.get("database")
            self.servers = kwargs.get("servers", [])

    def _read(self, path: Path) -> Optional[Dict]:
        try:
            with open(path) as f:
                match path.suffix:
                    case ".json":
                        return json.load(f)
                    case ".toml":
                        return toml.load(f)
                    case ".yaml":
                        return yaml.safe_load(f)
                    case _:
                        raise Exception("unknown extension '%s'" % path.suffix)
        except Exception as e:
            raise e

    def _parse(self, _dict: Dict) -> None:
        try:
            if database := _dict.get("database"):
                self.database = Database(**database)
            self.servers = [
                Server(**server)
                for server in _dict.get("servers", [])
                if isinstance(server, Dict)
            ]
        except Exception as e:
            raise e
