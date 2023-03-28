from typing import Dict
import toml

from consts import VALID_CONFIG_TEMPLATE, raw_config, invalid_raw_config


def from_file(path: str) -> Dict:
    try:
        with open(path) as f:
            return toml.load(f)
    except:
        return {}


def from_str(s: str) -> Dict:
    try:
        return toml.loads(s)
    except:
        return {}


def validate_section(config_section: Dict | None, valid_section: Dict) -> bool:
    if not isinstance(config_section, Dict):
        return False
    try:
        return all(
            isinstance(config_section.get(key), value_type)
            for key, value_type in valid_section.items()
        )
    except:
        return False


def valitate_config(config: Dict) -> bool:
    try:
        return all(
            validate_section(config.get(key), VALID_CONFIG_TEMPLATE[key])
            for key in VALID_CONFIG_TEMPLATE.keys()
        )
    except:
        return False


def print_config(title, config):
    print(
        "{t}\n{c}{s}\nvalid: {v}\n".format(
            t="{s} {t} {s}".format(s="-" * (14 - round(len(title) * 0.5)), t=title),
            s="-" * 30,
            c=toml.dumps(config),
            v=valitate_config(config),
        )
    )


def main():
    print_config("from_str", from_str(raw_config))
    print_config("from_file", from_file("config.toml"))
    print_config("from_str (invalid)", from_str(invalid_raw_config))


if __name__ == "__main__":
    main()
