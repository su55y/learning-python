from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import yaml


@dataclass
class Channel:
    title: str = ""
    channel_id: str = ""


@dataclass
class Config:
    channels: List[Channel]
    log_file: Optional[Path] = None
    log_stdout: bool = False

    def __init__(self, path_str: str) -> None:
        path = self._check_path(path_str)
        try:
            with open(path) as f:
                config = yaml.safe_load(f)
                self.channels = [Channel(**c) for c in config.pop("channels", [])]
                self.log_stdout = True if config.get("log_stdout") else False
                if log_file := config.get("log_file"):
                    self.log_file = Path(log_file)
        except Exception as e:
            exit(str(e))

    def _check_path(self, path_str) -> Path:
        path = Path(path_str)
        if not path.parent.exists() or not path.parent.is_dir():
            exit(f"{path.parent} not exists or not a directory")
        elif path.suffix == ".yaml" or path.suffix == ".yml":
            return path
        else:
            exit(f"invalid config path '{path}'")
