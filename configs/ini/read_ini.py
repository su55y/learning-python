import configparser
from typing import Dict, Tuple


def get_config(file: str, section: str) -> Tuple[Dict[str, str], Exception | None]:
    try:
        parser = configparser.ConfigParser()
        parser.read(file)
        if not parser.has_section(section):
            raise Exception(f"section '{section}' not found in '{file}'")

        return {k: v for k, v in parser.items(section)}, None
    except Exception as e:
        return {}, e
