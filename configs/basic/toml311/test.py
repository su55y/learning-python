import toml
import unittest

from config_loader import load_toml

valid_config = {'database': {'host': 'localhost', 'port': '3306', 'name': 'test_db'}}

class TestReadConfigFunction(unittest.TestCase):
    def test_config(self):
        config, err = load_toml("config.toml")
        self.assertIsNone(err)
        self.assertDictEqual(config, valid_config)
    def test_invalid_config(self):
        config, err = load_toml("invalid_config.toml")
        self.assertIsInstance(err, toml.TomlDecodeError)
        self.assertDictEqual(config, {})
    def test_not_found(self):
        config, err = load_toml("non_existent.toml")
        self.assertIsInstance(err, FileNotFoundError)
        self.assertDictEqual(config, {})
