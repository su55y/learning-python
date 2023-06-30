import configparser
import logging as log
from pathlib import Path
from typing import Dict, Tuple, Optional

from entities import Config, Database, Server, Servers
from my_config_loader import ConfigLoader


class DictLikeConfig(ConfigLoader):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

    def _parse(self, config_dict: Dict) -> Optional[Config]:
        try:
            return Config(
                database=Database(**config_dict["database"]),
                servers=Servers(
                    prod=Server(**config_dict["servers"]["prod"]),
                    test={
                        k: Server(**s)
                        for k, s in config_dict["servers"]["test"].items()
                    },
                ),
            )
        except Exception as e:
            log.error(f"parse_config_error: {repr(e)}, ({config_dict})")
            return None


class ConfigINI(ConfigLoader):
    _PREFIX_SERVER_PROD = "server_prod_"
    _PREFIX_SERVER_TEST_EXAMPLE = "server_test_example_"
    _PREFIX_SERVER_TEST_LOCALHOST = "server_test_localhost_"

    def __init__(self, path: Path, section: str) -> None:
        super().__init__(path, section)

    def _read(self) -> Tuple[Dict, Optional[Exception]]:
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

    def _parse(self, config_dict: Dict) -> Optional[Config]:
        try:
            if db_tables := config_dict.get("db_tables"):
                db_tables = db_tables.split()
            else:
                db_tables = []

            return Config(
                database=Database(
                    host=config_dict["db_host"],
                    port=config_dict["db_port"],
                    name=config_dict["db_name"],
                    tables=db_tables,
                ),
                servers=Servers(
                    prod=Server(
                        **{
                            k[len(self._PREFIX_SERVER_PROD) :]: v
                            for k, v in config_dict.items()
                            if k.startswith(self._PREFIX_SERVER_PROD)
                        }
                    ),
                    test={
                        "example.com": Server(
                            **{
                                k[len(self._PREFIX_SERVER_TEST_EXAMPLE) :]: v
                                for k, v in config_dict.items()
                                if k.startswith(self._PREFIX_SERVER_TEST_EXAMPLE)
                            }
                        ),
                        "localhost": Server(
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
