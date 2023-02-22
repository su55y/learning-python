from abc import abstractmethod
from typing import Dict, Tuple
import logging as log

from json import load as json_load
from toml import load as toml_load
from yaml import safe_load as yaml_load

from entities import config


class ConfigLoader:
    def __init__(self, path: str, section=None):
        self.path = path
        self.section = section

    def get_config(self) -> config.Config | None:
        config_dict, err = self._read()
        if err:
            log.error(f"read config error: {repr(err)}")
            return None

        return self._parse(config_dict)

    @abstractmethod
    def _parse(self, config_dict: Dict) -> config.Config | None:
        ...

    def _read(self) -> Tuple[Dict, Exception | None]:
        try:
            with open(self.path) as f:
                match self.path.split(".")[-1]:
                    case "json":
                        return json_load(f), None
                    case "toml":
                        return toml_load(f), None
                    case "yaml":
                        return yaml_load(f), None
                    case _:
                        return {}, Exception("unknown extension")
        except Exception as e:
            return {}, e
