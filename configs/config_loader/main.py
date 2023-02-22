from my_config_loader.parsers import DictLikeConfig, ConfigINI
from entities import entities


JSON_FILE = "config.json"
TOML_FILE = "config.toml"
YAML_FILE = "config.yaml"
INI_FILE = "config.ini"
INI_SECTION = "config"


def main():
    json_config = DictLikeConfig(JSON_FILE).get_config()
    toml_config = DictLikeConfig(TOML_FILE).get_config()
    yaml_config = DictLikeConfig(YAML_FILE).get_config()
    ini_config = ConfigINI(INI_FILE, INI_SECTION).get_config()

    if not json_config or not toml_config or not yaml_config or not ini_config:
        exit(1)

    print(json_config == toml_config == yaml_config == ini_config)
    print(
        ini_config.servers.prod
        == entities.Server(
            host=json_config.servers.prod.host,
            port=toml_config.servers.prod.port,
            url=yaml_config.servers.prod.url,
        )
    )


if __name__ == "__main__":
    main()
