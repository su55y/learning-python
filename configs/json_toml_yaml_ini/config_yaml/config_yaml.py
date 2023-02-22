from typing import Dict, Tuple
from entities import config, entities
import logging as log
import yaml


def get_yaml_config(file: str) -> config.Config | None:
    config_dict, err = _read_config(file)
    if err:
        log.error(f"read yaml config error: {repr(err)}")
        return None

    return _parse_config(config_dict)


def _read_config(file: str) -> Tuple[Dict, Exception | None]:
    try:
        with open(file) as f:
            return yaml.safe_load(f), None
    except Exception as e:
        return {}, e


def _parse_config(config_dict: Dict) -> config.Config | None:
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
        log.error(f"parse_ini_config_error: {repr(e)}, ({config_dict})")
        return None
