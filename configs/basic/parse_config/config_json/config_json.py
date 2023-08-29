from typing import Dict, Tuple, Optional
from entities import config, entities
import logging as log
import json


def get_json_config(file: str) -> Optional[config.Config]:
    config_dict, err = _read_config(file)
    if err:
        log.error(f"read json config error: {repr(err)}")
        return None

    return _parse_config(config_dict)


def _read_config(file: str) -> Tuple[Dict, Optional[Exception]]:
    try:
        with open(file) as f:
            return json.load(f), None
    except Exception as e:
        return {}, e


def _parse_config(config_dict: Dict) -> Optional[config.Config]:
    try:
        return config.Config(
            database=entities.Database(**config_dict["database"]),
            servers=entities.Servers(
                prod=entities.Server(**config_dict["servers"]["prod"]),
                test={
                    k: entities.Server(**s)
                    for k, s in config_dict["servers"]["test"].items()
                },
            ),
        )
    except Exception as e:
        log.error(f"parse_json_config_error: {repr(e)}, ({config_dict})")
        return None
