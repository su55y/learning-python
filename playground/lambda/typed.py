from collections.abc import Callable
from typing import List, Tuple


if __name__ == "__main__":
    nums: List[int] = [1, 2, 3]

    half: Callable[[int], float] = lambda n: n * 0.5
    combine_with_half: Callable[[int], Tuple[int, float]] = lambda n: (n, half(n))

    half_nums: List[float] = list(map(half, nums))
    nums_combined: List[Tuple[int, float]] = list(map(combine_with_half, nums))

    print("nums:", nums)
    print("half_nums:", half_nums)

    print_combined: Callable[[int, float], None] = lambda i, f: print(f"{i}: {f}")
    _ = print("combined:") or [print_combined(i, f) for i, f in nums_combined]
