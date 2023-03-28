VALID_DB_CONFIG = {
    "database": {
        "host": str,
        "port": int,
    },
    "server": {
        "host": str,
        "ports": list,
        "timeout": float,
    },
}

raw_config = """
[database]
host = "localhost"
port = 3306

[server]
host = "https://test.example.com"
ports = [1337, 443]
timeout = 13.37
"""

invalid_raw_config = """
[database]
host = "localhost"
port = 3306

[server]
host = "https://test.example.com"
ports = [1337, 443]
timeout = "13,37"
"""
