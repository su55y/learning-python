import itertools as it


def product(length=5):
    foo = ""
    for i in range(length):
        for j in range(length):
            foo += f"{i}{j}"
    baz = "".join([f"{i}{j}" for i in range(length) for j in range(length)])
    bar = "".join([f"{i}{j}" for i, j in it.product(range(length), repeat=2)])
    assert foo == bar
    assert foo == baz
    assert baz == bar
    print(f"product:\n{foo = }\n{bar = }")


def permutations(length=5):
    foo = ""
    for i in range(length):
        for j in range(length):
            if i != j:
                foo += f"{i}{j}"

    bar = "".join([f"{i}{j}" for i, j in it.permutations(range(length), 2)])
    assert foo == bar
    print(f"permutations:\n{foo = }\n{bar = }")


def combinations(length=8):
    foo = ""
    for i in range(length):
        for j in range(i + 1, length):
            foo += f"{i}{j}"

    bar = "".join([f"{i}{j}" for i, j in it.combinations(range(length), 2)])
    assert foo == bar
    print(f"combinations:\n{foo = }\n{bar = }")


def combinations_with_replacement(length=8):
    foo = ""
    for i in range(length):
        for j in range(i, length):
            foo += f"{i}{j}"

    bar = "".join(
        [f"{i}{j}" for i, j in it.combinations_with_replacement(range(length), 2)]
    )
    assert foo == bar
    print(f"combinations_with_replacement:\n{foo = }\n{bar = }")


if __name__ == "__main__":
    product()
    permutations()
    combinations()
    combinations_with_replacement()
