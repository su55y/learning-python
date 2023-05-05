from time import perf_counter


def countdown(n: int):
    print(f"counting down from {n}")
    while n > 0:
        n -= 1


def main():
    COUNT = 100_000_000
    countdown(COUNT)


if __name__ == "__main__":
    start = perf_counter()
    main()
    print(f"done in {perf_counter() - start:.02f}s")
