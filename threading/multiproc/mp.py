import multiprocessing as mp
from time import perf_counter


def countdown(n: int, proc_name: str):
    print(f"{proc_name} counting down from {n}")
    while n > 0:
        n -= 1

def main():
    CPU_COUNT = mp.cpu_count()
    print(f"cpu count: {CPU_COUNT}")
    COUNTDOWN_VALUE = 100_000_000 // CPU_COUNT
    proc_list = [
        mp.Process(target=countdown, args=(COUNTDOWN_VALUE,f"proc#{i}"), name=f"proc#{i}")
        for i in range(CPU_COUNT)
    ]

    for p in proc_list:
        print(f"start process {p.name}")
        p.start()
    for p in proc_list:
        p.join()
        print(f"process {p.name} done")


if __name__ == "__main__":
    start = perf_counter()
    main()
    print(f"done in {perf_counter() - start:.02f}s")
