import os


def get_uptime():
    try:
        with open("/proc/uptime") as f:
            val = float(f.readline().split()[0])
        days = int(val / 60 / 60 / 24)
        hours = int(val / 60 / 60 % 24)
        mins = int(val / 60 % 60)
    except:
        return "Unknown"

    if days > 0:
        return f"{days} day{'s' if days > 1 else ''}, {hours} hour{'' if hours == 1 else 's' }, {mins} min{'' if mins == 1 else 's'}"
    elif hours > 0:
        return f"{hours} hour{'' if hours == 1 else 's' }, {mins} min{'' if mins == 1 else 's'}"
    else:
        return f"{mins} min{'' if mins == 1 else 's'}"

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
    tab = " " * 4
    distro_l = f"\033[33mOS\033[0m{tab}"
    shell_l = f"\033[34mShell\033[0m{tab}"
    uptime_l = f"\033[35mUptime\033[0m{tab}"
    title = get_title().strip()
    distro = get_distro().strip()
    shell = get_shell().strip()
    palette = get_palette()
    uptime = get_uptime()
    max_len = max(map(len, [distro_l, shell_l, shell, distro, uptime]))
    print(f"{title: >{9+len(title)}}")
    print(f"*---*{tab}{'-'*len(title)}")
    print(f"| F |{tab}{distro_l: <{max_len}}{distro.strip("\"")}")
    print(f"*---*{tab}{shell_l: <{max_len}}{shell}")
    print(f"     {tab}{uptime_l: <{max_len}}{uptime}")
    print()
    for colors in palette:
        print(f"{colors: >{len(colors) + 8}}")
