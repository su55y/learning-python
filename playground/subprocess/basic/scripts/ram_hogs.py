import subprocess as sp
from sys import argv
from typing import Dict, List, Tuple

COUNT = 10
CMD = "ps axch -o cmd,%mem --sort=-%mem"

def get_ps_output() -> List[str]:
    if out := sp.getoutput(CMD):
        return out.splitlines()
    exit("can't get output from ps")


def parse_output(out: List[str]) -> List[Tuple[str, float]]:
    procs: Dict[str, float] = {}
    for line in out:
        name, *_, perc = line.split()
        procs[name] = procs[name] + float(perc) if procs.get(name) else float(perc)
    return sorted(procs.items(), key=lambda x: x[-1], reverse=True)


if __name__ == "__main__":
    if argv[1:]:
        try:
            COUNT = int(argv[-1])
        except:
            pass

    print("\n".join(f"{name}: {perc:.1f}%" for name, perc in parse_output(get_ps_output())[:COUNT]))
