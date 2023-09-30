import subprocess as sp
from sys import argv

LIMIT = 10
CMD = "ps axch -o cmd,%mem --sort=-%mem"
HELP = """usage: ram_hogs [-h] [LIMIT]
Shows the top ram hogs using ps command. Default LIMIT is 10"""

if __name__ == "__main__":
    args = argv[1:]
    if "-h" in args or "--help" in args or len(args) > 1:
        print(HELP)
        exit(0)
    if args:
        try:
            LIMIT = int(argv[1])
        except:
            pass

    procs = {}
    for line in sp.getoutput(CMD).splitlines():
        name, *_, perc = line.split()
        procs[name] = procs[name] + float(perc) if procs.get(name) else float(perc)

    sorted_procs = sorted(procs.items(), key=lambda x: x[-1], reverse=True)[:LIMIT]
    max_width = max(len(name) for name, _ in sorted_procs) + 1
    for name, perc in sorted_procs:
        print(f"{name:{max_width}}", f"{perc:.1f}%".rjust(5))
