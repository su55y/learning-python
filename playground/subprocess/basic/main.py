import asyncio
from pathlib import Path
import subprocess as sp
import sys


print_dates_path = Path(__file__).parent / "print_dates.sh"


def getoutput_with_pipe() -> str:
    return sp.getoutput(f"{print_dates_path} | grep -oP '\\d{{4}}'")


def sp_run() -> int:
    return sp.run(print_dates_path).returncode


def popen_wait_check_output() -> int:
    proc = sp.Popen(str(print_dates_path), stdout=sp.PIPE, shell=True)
    out = sp.check_output(["grep", "-oP", "\\d{4}"], stdin=proc.stdout)
    sys.stdout.write(out.decode())
    return proc.wait()


async def async_sp() -> int:
    proc = await asyncio.create_subprocess_exec(
        print_dates_path, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    out, err = await proc.communicate()
    if out:
        sys.stdout.write(out.decode())
    if err:
        sys.stdout.write(err.decode())

    return 1 if proc.returncode is None else proc.returncode


def main():
    if not print_dates_path.exists():
        print("test executable not found")
        exit(1)

    print("# run()")
    print(f"exit with code: {sp_run()}")

    print("\n# Popen().wait()")
    print(f"exit with code: {popen_wait_check_output()}")

    print("\n# getoutput()")
    print(getoutput_with_pipe())

    print("\n# async_sp()")
    print(f"exit with code: {asyncio.run(async_sp())}")


if __name__ == "__main__":
    main()
