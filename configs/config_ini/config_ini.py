import configparser
from typing import Dict, Tuple
from entities import config, entities
import logging as log

PREFIX_SERVER_PROD = "server_prod_"
PREFIX_SERVER_TEXT_EXAMPLE = "server_test_example_"
PREFIX_SERVER_TEST_LOCALHOST = "server_test_localhost_"


def get_ini_config(file: str, section: str) -> config.Config | None:
    config_dict, err = _read_config(file, section)
    if err:
        log.error(f"read ini config error: {repr(err)}")
        return None

    return _parse_config(config_dict)


def _read_config(file: str, section: str) -> Tuple[Dict[str, str], Exception | None]:
    try:
        parser = configparser.ConfigParser()
        parser.read(file)
        if not parser.has_section(section):
            raise Exception(f"section '{section}' not found in '{file}'")

        return {k: v for k, v in parser.items(section)}, None
    except Exception as e:
        return {}, e


def _parse_config(config_dict: Dict[str, str]) -> config.Config | None:
    try:
        if db_tables := config_dict.get("db_tables"):
            db_tables = db_tables.split()
        else:
            db_tables = []

        return config.Config(
            database=entities.Database(
                host=config_dict["db_host"],
                port=config_dict["db_port"],
                name=config_dict["db_name"],
                tables=db_tables,
            ),
            servers=entities.Servers(
                prod=entities.Server(
                    **{
                        k[len(PREFIX_SERVER_PROD) :]: v
                        for k, v in config_dict.items()
                        if k.startswith(PREFIX_SERVER_PROD)
                    }
                ),
                test={
                    "example.com": entities.Server(
                        **{
                            k[len(PREFIX_SERVER_TEXT_EXAMPLE) :]: v
                            for k, v in config_dict.items()
                            if k.startswith(PREFIX_SERVER_TEXT_EXAMPLE)
                        }
                    ),
                    "localhost": entities.Server(
                        **{
                            k[len(PREFIX_SERVER_TEST_LOCALHOST) :]: v
                            for k, v in config_dict.items()
                            if k.startswith(PREFIX_SERVER_TEST_LOCALHOST)
                        },
                    ),
                },
            ),
        )
    except Exception as e:
        log.error(f"parse_ini_config_error: {repr(e)}, ({config_dict})")
        return None
