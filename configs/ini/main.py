from configparser import ConfigParser
from typing import Dict, Tuple


def get_config(
    file="config.ini", section="config"
) -> Tuple[Dict[str, str], Exception | None]:
    config = {}
    err = None
    parser = ConfigParser()

    try:
        parser.read(file)
    except Exception as e:
        err = e
    else:
        if parser.has_section(section):
            for k, v in parser.items(section):
                config[k] = v
        else:
            err = Exception(f"section '{section}' not found in '{file}'")
    finally:
        return config, err


def main():
    config, err = get_config()
    if err is not None:
        print(repr(err))
    else:
        print(config)


if __name__ == "__main__":
    main()
