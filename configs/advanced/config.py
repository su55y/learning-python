from dataclasses import dataclass, field
import json
from pathlib import Path
import toml
from typing import Dict, List, Optional

import yaml

from entities import Database, Server


class UnknownFileExtException(Exception):
    pass


class InvalidConfigException(Exception):
    pass


@dataclass(eq=True)
class Config:
    database: Database
    servers: List[Server] = field(default_factory=list)

    def __init__(
        self,
        database: Optional[Database] = None,
        servers: Optional[List[Server]] = None,
        path: Optional[Path] = None,
    ) -> None:
        if path:
            if not path.exists() or path.is_dir():
                raise FileNotFoundError("%s not found" % path)
            if not (config_dict := self._read(path)):
                raise InvalidConfigException("")
            self._parse(config_dict)
        elif servers is not None and database is not None:
            self.database = database
            self.servers = servers
        else:
            raise InvalidConfigException("path or config properties are missing")

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
                        raise UnknownFileExtException(
                            "unknown extension '%s'" % path.suffix
                        )
        except Exception as e:
            raise e

    def _parse(self, config_dict: Dict) -> None:
        try:
            database = config_dict.get("database")
            if not database or not isinstance(database, Dict):
                raise InvalidConfigException("database are required")
            servers = config_dict.get("servers")
            if servers is None or not isinstance(servers, List):
                raise InvalidConfigException("servers are required")
            self.database = Database(**database)
            self.servers = [
                Server(**server) for server in servers if isinstance(server, Dict)
            ]
        except Exception as e:
            raise e
