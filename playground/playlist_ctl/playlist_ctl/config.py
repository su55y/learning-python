from dataclasses import dataclass
import logging
from os.path import expandvars
from pathlib import Path
import tomllib
from typing import Dict, Optional

from playlist_ctl import defaults


@dataclass
class Config:
    log_file: Path
    log_level: int
    socket_file: Path
    storage_file: Path

    def __init__(
        self,
        config_file: Optional[Path] = None,
        log_file: Optional[Path] = None,
        log_level: Optional[int] = None,
        socket_file: Optional[Path] = None,
        storage_file: Optional[Path] = None,
    ) -> None:
        self.log_file = log_file or defaults.default_logfile_path()
        self.log_level = log_level or 0
        self.socket_file = socket_file or defaults.default_socket_path
        self.storage_file = storage_file or defaults.default_storage_path()
        if config_file:
            config_file = Path(expandvars(config_file.expanduser()))
            if not config_file.exists():
                return
            config = self._read_from_file(config_file)
            if log_file := config.get("log_file"):
                self.log_file = log_file
            if log_level := config.get("log_level"):
                self.log_level = self._choose_log_level(log_level)
            if socket_file := config.get("socket_file"):
                self.socket_file = socket_file
            if storage_file := config.get("storage_file"):
                self.storage_file = storage_file

    def _read_from_file(self, file: Path) -> Dict:
        try:
            with open(file, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            logging.critical(msg := "can't read config %s: %s" % (file, e))
            exit(msg)

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
