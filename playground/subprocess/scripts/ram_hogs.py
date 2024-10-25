import subprocess as sp
from sys import argv

LIMIT = 10
CMD = "ps axch -o cmd,%mem --sort=-%mem"
HELP = f"""usage: ram_hogs [-h] [LIMIT]
Shows the top ram hogs using ps command.

positional arguments:
    LIMIT       lines count to show, default: {LIMIT}"""


def exit_with_help():
    print(HELP)
    exit(0)


if __name__ == "__main__":
    args = argv[1:]

    if len(args) > 1:
        exit_with_help()

    if len(args) == 1:
        arg = args[0]
        match arg:
            case "-h" | "--help":
                exit_with_help()
        try:
            LIMIT = int(arg)
            if LIMIT < 1:
                raise ValueError()
        except Exception as e:
            if isinstance(e, ValueError):
                print(f"ERROR: Invalid LIMIT value {arg!r}, should be positive integer")
            exit_with_help()

    procs = {}
    for line in sp.getoutput(CMD).splitlines():
        name, *_, perc = line.split()
        procs[name] = procs[name] + float(perc) if procs.get(name) else float(perc)

    sorted_procs = sorted(procs.items(), key=lambda x: x[-1], reverse=True)[:LIMIT]
    max_width = max(len(name) for name, _ in sorted_procs) + 1
    for name, perc in sorted_procs:
        print(f"{name:{max_width}}", f"{perc:.1f}%".rjust(5))
