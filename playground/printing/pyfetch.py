import os


def get_title() -> str:
    username = os.getlogin()
    uname = os.uname()
    return f"\033[32m{username}\033[0m@\033[32m{uname.nodename}\033[0m"


def get_kernel() -> str:
    uname = os.uname()
    return uname.release


def get_distro() -> str:
    release_info = {}
    with open("/etc/os-release") as f:
        for line in f.readlines():
            key, value = line.split("=")
            release_info[key] = value
    return release_info.get("NAME", "Unknown")


def get_shell() -> str:
    return os.environ.get("SHELL", "Unknown").split("/").pop()


def get_palette() -> list[str]:
    fg = "".join(f"\033[4{i}m   \033[0m" for i in range(8))
    bg = "".join(f"\033[10{i}m   \033[0m" for i in range(8))
    return [fg, bg]

if __name__ == "__main__":
    distro_l = "\033[33mOS\033[0m    "
    shell_l = "\033[34mShell\033[0m    "
    title = get_title().strip()
    distro = get_distro().strip()
    shell = get_shell().strip()
    palette = get_palette()
    max_len = max(map(len, [distro_l, shell_l, shell, distro]))
    print(f"{title: >{8 + len(title)}}")
    print("*---*   " + "-" * len(title))
    print("| F |   " + f"{distro_l: <{max_len}}{distro.strip("\"")}")
    print("*---*   " + f"{shell_l: <{max_len}}{shell}")
    print()
    for colors in palette:
        print(f"{colors: >{len(colors) + 8}}")
