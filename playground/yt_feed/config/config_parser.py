import logging
from pathlib import Path
from os import getenv
from typing import Optional

import yaml

from models import Config, Channel


class ConfigParser:
    def __init__(self, path=None) -> None:
        self.log = logging.getLogger()
        self._path = path
        self._set_default_config_path()

    @property
    def default_config_path(self) -> Path:
        return self.__default_config_path

    def get_config(self) -> Optional[Config]:
        if path := self._get_path():
            try:
                with open(path) as f:
                    config = yaml.safe_load(f)
                    channels = [Channel(**c) for c in config.get("channels", [])]
                    return Config(channels=channels)

            except Exception as e:
                self.log.error(e)

    def _get_path(self) -> Optional[Path]:
        path = Path(self._path) if self._path else self.default_config_path
        if not path.parent.exists() or path.parent.is_dir():
            self.log.error(f"{path.parent} not exists or not a directory")
        elif path.suffix == ".yaml" or path.suffix == ".yml":
            return path
        else:
            self.log.error(f"invalid config path '{path}'")

    def _set_default_config_path(self, config_name="config.yaml"):
        config_home = None
        if xdg_config_home := getenv("XDG_CONFIG_HOME"):
            config_home = Path(xdg_config_home)
        else:
            config_home = Path.joinpath(Path.home(), ".config")

        self.__default_config_path = Path.joinpath(config_home, "pyt-feed", config_name)
