from os.path import dirname, exists
from subprocess import getoutput, run, Popen


EXE = f"{dirname(__file__)}/print_dates.sh"


def getoutput_with_pipe() -> str:
    grep_year = "grep -oP '\\d{4}'"
    return getoutput(f"{EXE} | {grep_year}")


def sp_run() -> int:
    return run([EXE]).returncode


def popen_wait() -> int:
    return Popen(EXE).wait()


def main():
    if not exists(EXE):
        print("test executable not found")
        exit(1)

    print("# run()")
    print(f"exit with code: {sp_run()}")

    print("\nPopen().wait()")
    print(f"exit with code: {popen_wait()}")

    print("\n# getoutput()\n", getoutput_with_pipe(), sep="")


if __name__ == "__main__":
    main()
