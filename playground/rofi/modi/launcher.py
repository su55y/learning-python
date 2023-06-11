from pathlib import Path
from subprocess import run

PANDA = "\U0001F43C"
ROFI_BASE_CMD = f"rofi -show {PANDA} -modi {PANDA}:%s -no-config -kb-custom-1 Ctrl+s"


if __name__ == "__main__":
    modi_path = Path(Path(__file__).resolve().parent).joinpath("modi.py")
    if not modi_path.exists():
        exit(f"{modi_path} not exists")
    run((ROFI_BASE_CMD % modi_path).split())
