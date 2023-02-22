from config_ini import config_ini
from config_json import config_json
from config_yaml import config_yaml
from config_toml import config_toml
from entities import entities

INI_FILE = "config_ini/config.ini"
INI_SECTION = "config"
JSON_FILE = "config_json/config.json"
YAML_FILE = "config_yaml/config.yaml"
TOML_FILE = "config_toml/config.toml"


def main():
    json_config = config_json.get_json_config(JSON_FILE)
    toml_config = config_toml.get_toml_config(TOML_FILE)
    yaml_config = config_yaml.get_yaml_config(YAML_FILE)
    ini_config = config_ini.get_ini_config(INI_FILE, INI_SECTION)

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
