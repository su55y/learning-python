#!/usr/bin/env -S python3 -u


def get_true() -> bool:
    return True


def get_false() -> bool:
    return False


def div(x: int | float, y: int | float) -> Exception | None:
    try:
        x / y
    except Exception as e:
        return e
    else:
        return None


class Result:
    def __init__(self, result: int | float | None, err: Exception | None) -> None:
        self.result = result
        self.err = err


def div_with_result(x: int | float, y: int | float) -> Result:
    try:
        r = x / y
    except Exception as e:
        return Result(None, e)
    else:
        return Result(r, None)


def main():
    if ok := get_true():
        print(f"get_true() returns {ok}")

    if not (not_ok := get_false()):
        print(f"get_false() returns {not_ok}")

    if err := div(0, 0):
        print(f"division error: {repr(err)}")

    if not (err := div(1, 1)):
        print("1/1 division is allowed")

    if (res := div_with_result(2, 0)) and res.err:
        print(f"division error: {repr(res.err)}")

    if (res := div_with_result(1, 2)) and not res.err:
        print(f"division result: {res.result}")


if __name__ == "__main__":
    main()
