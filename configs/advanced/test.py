from pathlib import Path

from config import Config
from entities import Database, Server


if __name__ == "__main__":
    config_sample = Config(
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
                name="prod", host="77.77.77.77", port="80", url="https://example.com/"
            ),
        ],
    )

    assert Config(Path("configs/config.json")) == config_sample, "invalid json config"
    assert Config(Path("configs/config.toml")) == config_sample, "invalid toml config"
    assert Config(Path("configs/config.yaml")) == config_sample, "invalid yaml config"
