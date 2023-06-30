from abc import abstractmethod
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging as log

from json import load as json_load
from toml import load as toml_load
from yaml import safe_load as yaml_load

from entities import Config


class ConfigLoader:
    def __init__(self, path: Path, section=None) -> None:
        self.path = path
        self.section = section

    @property
    def config(self) -> Optional[Config]:
        config_dict, err = self._read()
        if err:
            log.error(f"read config error: {err}")
            return

        return self._parse(config_dict)

    @abstractmethod
    def _parse(self, config_dict: Dict) -> Optional[Config]:
        ...

    def _read(self) -> Tuple[Dict, Optional[Exception]]:
        try:
            with open(self.path) as f:
                match self.path.suffix:
                    case ".json":
                        return json_load(f), None
                    case ".toml":
                        return toml_load(f), None
                    case ".yaml":
                        return yaml_load(f), None
                    case _:
                        return {}, Exception("unknown extension")
        except FileNotFoundError:
            exit("%s not found" % self.path)
        except Exception as e:
            return {}, e
