from dataclasses import dataclass
import logging
from os.path import expandvars
from pathlib import Path
import tomllib
from typing import Dict, Optional

from playlist_ctl import defaults


@dataclass
class Config:
    cache_dir: Path
    log_file: Path
    log_level: int
    socket_file: Path
    storage_file: Path

    def __init__(
        self,
        config_file: Optional[Path] = None,
        cache_dir: Optional[Path] = None,
        log_file: Optional[Path] = None,
        log_level: Optional[int] = None,
        socket_file: Optional[Path] = None,
        storage_file: Optional[Path] = None,
    ) -> None:
        self.cache_dir = cache_dir or defaults.default_cachedir_path()
        self.log_file = log_file or self.cache_dir.joinpath("playlist_ctl.log")
        self.log_level = log_level or 0
        self.socket_file = socket_file or defaults.default_socket_path
        self.storage_file = storage_file or self.cache_dir.joinpath("playlist_ctl.db")
        if config_file:
            config_file = Path(expandvars(config_file.expanduser()))
            if not config_file.exists():
                return
            config = self._read_from_file(config_file)
            if log_level_ := config.get("log_level"):
                self.log_level = self._choose_log_level(log_level_)
            if cache_dir_ := config.get("cache_dir"):
                self.cache_dir = Path(cache_dir_)
                self.log_file = self.cache_dir.joinpath("playlist_ctl.log")
                self.storage_file = self.cache_dir.joinpath("playlist_ctl.db")
            if socket_file_ := config.get("socket_file"):
                self.socket_file = Path(socket_file_)

    def _read_from_file(self, file: Path) -> Dict:
        try:
            with open(file, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            exit("can't read config %s: %s" % (file, e))

    def _choose_log_level(self, lvl: str) -> int:
        match lvl:
            case "debug" | "DEBUG":
                return logging.DEBUG
            case "info" | "INFO":
                return logging.INFO
            case "warning" | "WARNING":
                return logging.WARNING
            case "error" | "ERROR":
                return logging.ERROR
        return 0
