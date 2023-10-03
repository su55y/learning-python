from functools import wraps

count = 0


def with_counter_wraps(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global count
        count += 1
        return f(*args, **kwargs)

    return wrapper


@with_counter_wraps
def add_wraps(a, b):
    """Docstring wraps"""
    return a + b


def with_counter_no_wraps(f):
    def wrapper(*args, **kwargs):
        global count
        count += 1
        return f(*args, **kwargs)

    return wrapper


@with_counter_no_wraps
def add_no_wraps(a, b):
    """Docstring no wraps"""
    return a + b


if __name__ == "__main__":
    _ = sum(add_wraps(n, n) for n in range(5))
    assert count == 5
    assert add_wraps.__name__ == "add_wraps"
    print(f"add_wraps.__name__ == {add_wraps.__name__!r}")
    assert add_wraps.__doc__ == "Docstring wraps"
    print(f"add_wraps.__doc__ == {add_wraps.__doc__!r}")
    _ = sum(add_no_wraps(n, n) for n in range(5))
    assert count == 10
    assert add_no_wraps.__name__ == "wrapper"
    print(f"add_no_wraps.__name__ == {add_no_wraps.__name__!r}")
    assert add_no_wraps.__doc__ is None
    print(f"add_no_wraps.__doc__ is {add_no_wraps.__doc__!r}")
