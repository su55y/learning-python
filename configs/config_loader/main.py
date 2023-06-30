from pathlib import Path

from my_config_loader import DictLikeConfig, ConfigINI
from entities import Config, Database, Server, Servers


if __name__ == "__main__":
    config_sample = Config(
        database=Database(
            host="localhost",
            port="3306",
            name="test_db",
            tables=["tb_countries", "tb_continents"],
        ),
        servers=Servers(
            prod=Server(host="77.77.77.77", port="80", url="https://example.com/"),
            test={
                "example.com": Server(
                    host="31.33.77.77", port="1337", url="https://test.example.com/"
                ),
                "localhost": Server(host="127.0.0.1", port="1337"),
            },
        ),
    )

    json_config = DictLikeConfig(Path("config.json")).config
    assert json_config == config_sample, "invalid json config"

    toml_config = DictLikeConfig(Path("config.toml")).config
    assert toml_config == config_sample, "invalid toml config"

    yaml_config = DictLikeConfig(Path("config.yaml")).config
    assert yaml_config == config_sample, "invalid yaml config"

    ini_config = ConfigINI(Path("config.ini"), section="config").config
    assert ini_config == config_sample, "invalid ini config"

    print("ok")
