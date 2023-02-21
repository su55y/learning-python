from ini.read_ini import get_config

ini_file = "config.ini"
ini_section = "config"


def main():
    ini_config, err = get_config(ini_file, ini_section)
    if not err:
        print(ini_config)
    else:
        print(repr(err))


if __name__ == "__main__":
    main()
