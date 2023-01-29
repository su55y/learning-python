from os.path import dirname, exists
from subprocess import PIPE, check_output, getoutput, run, Popen


EXE = f"{dirname(__file__)}/print_dates.sh"


def getoutput_with_pipe() -> str:
    grep_year = "grep -oP '\\d{4}'"
    return getoutput(f"{EXE} | {grep_year}")


def sp_run() -> int:
    return run([EXE]).returncode


def popen_wait_check_output() -> int:
    p = Popen(EXE, stdout=PIPE, shell=True)
    o = check_output(["grep", "--color=never", "-oP", "\\d{4}"], stdin=p.stdout)
    print(o.decode(), end="")
    return p.wait()


def main():
    if not exists(EXE):
        print("test executable not found")
        exit(1)

    print("# run()")
    print(f"exit with code: {sp_run()}")

    print("\n# Popen().wait()")
    print(f"exit with code: {popen_wait_check_output()}")

    print("\n# getoutput()")
    print(getoutput_with_pipe())


if __name__ == "__main__":
    main()
