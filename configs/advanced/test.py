from pathlib import Path
import unittest

from config import Config, UnknownFileExtException, InvalidConfigException
from entities import Database, Server


class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config_sample = Config(
            database=Database(
                host="localhost",
                port="3306",
                name="test_db",
                tables=["tb_countries", "tb_continents"],
            ),
            servers=[
                Server(
                    name="test example.com",
                    host="31.33.77.77",
                    port="1337",
                    url="https://test.example.com/",
                ),
                Server(name="test localhost", host="127.0.0.1", port="1337"),
                Server(
                    name="prod",
                    host="77.77.77.77",
                    port="80",
                    url="https://example.com/",
                ),
            ],
        )

    def test_json_config(self):
        self.assertEqual(Config(path=Path("configs/config.json")), self.config_sample)

    def test_toml_config(self):
        self.assertEqual(Config(path=Path("configs/config.toml")), self.config_sample)

    def test_yaml_config(self):
        self.assertEqual(Config(path=Path("configs/config.yaml")), self.config_sample)

    def test_invalid_path(self):
        self.assertRaises(FileNotFoundError, Config, path=Path("-"))

    def test_invalid_extension(self):
        self.assertRaises(
            UnknownFileExtException, Config, path=Path("configs/config.ini")
        )

    def test_invalid_config1(self):
        self.assertRaises(InvalidConfigException, Config)

    def test_invalid_config2(self):
        dummy_db = Database("a", "b", "c", [])
        self.assertRaises(InvalidConfigException, Config, database=dummy_db)

    def test_invalid_config3(self):
        self.assertRaises(InvalidConfigException, Config, servers=[])
