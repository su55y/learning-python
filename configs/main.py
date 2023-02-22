from config_ini import config_ini
from config_json import config_json

INI_FILE = "config_ini/config.ini"
INI_SECTION = "config"
JSON_FILE = "config_json/config.json"


def print_ini():
    ini_config = config_ini.get_ini_config(INI_FILE, INI_SECTION)
    if ini_config:
        print(ini_config)
        print(ini_config.servers.prod.host)


def print_json():
    json_config = config_json.get_json_config(JSON_FILE)
    if json_config:
        print(json_config)
        print(json_config.servers.prod.host)


def main():
    print_ini()
    print_json()


if __name__ == "__main__":
    main()
