import toml
from typing import Dict, Optional, Tuple

def load_toml(path) -> Tuple[Dict, Optional[Exception]]:
    try:
        with open(path) as f:
            return toml.load(f), None
    except Exception as e:
        if isinstance(e, toml.TomlDecodeError):
            e.args = (f"Invalid TOML: {e}",)
        return {}, e
