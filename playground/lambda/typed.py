from collections.abc import Callable
from typing import List, Tuple


def main():
    nums: List[int] = [1, 2, 3]

    half: Callable[[int], float] = lambda n: n * 0.5
    combine_with_half: Callable[[int], Tuple[int, float]] = lambda n: (n, half(n))

    half_nums: List[float] = list(map(half, nums))
    nums_combined: List[Tuple[int, float]] = list(map(combine_with_half, nums))

    print("nums:", nums)
    print("half_nums:", half_nums)
    print("combined:")
    for (i, f) in nums_combined:
        print(f"\t({i}({type(i).__name__}), {f}({type(f).__name__}))")


if __name__ == "__main__":
    main()
