from typing import Dict, Tuple
from entities import entities, config
import configparser
import logging as log

from my_config_loader.loader import ConfigLoader


class DictLikeConfig(ConfigLoader):
    def __init__(self, path: str):
        super().__init__(path)

    def _parse(self, config_dict: Dict) -> config.Config | None:
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
            log.error(f"parse_config_error: {repr(e)}, ({config_dict})")
            return None


class ConfigINI(ConfigLoader):
    _PREFIX_SERVER_PROD = "server_prod_"
    _PREFIX_SERVER_TEXT_EXAMPLE = "server_test_example_"
    _PREFIX_SERVER_TEST_LOCALHOST = "server_test_localhost_"

    def __init__(self, path: str, section: str):
        super().__init__(path, section)

    def _read(self) -> Tuple[Dict, Exception | None]:
        try:
            if not self.section:
                raise Exception("section must be set")

            parser = configparser.ConfigParser()
            parser.read(self.path)
            if not parser.has_section(self.section):
                raise Exception(f"section '{self.section}' not found in '{self.path}'")

            return {k: v for k, v in parser.items(self.section)}, None
        except Exception as e:
            return {}, e

    def _parse(self, config_dict: Dict) -> config.Config | None:
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
                            k[len(self._PREFIX_SERVER_PROD) :]: v
                            for k, v in config_dict.items()
                            if k.startswith(self._PREFIX_SERVER_PROD)
                        }
                    ),
                    test={
                        "example.com": entities.Server(
                            **{
                                k[len(self._PREFIX_SERVER_TEXT_EXAMPLE) :]: v
                                for k, v in config_dict.items()
                                if k.startswith(self._PREFIX_SERVER_TEXT_EXAMPLE)
                            }
                        ),
                        "localhost": entities.Server(
                            **{
                                k[len(self._PREFIX_SERVER_TEST_LOCALHOST) :]: v
                                for k, v in config_dict.items()
                                if k.startswith(self._PREFIX_SERVER_TEST_LOCALHOST)
                            },
                        ),
                    },
                ),
            )
        except Exception as e:
            log.error(f"parse_ini_config_error: {repr(e)}, ({config_dict})")
            return None
