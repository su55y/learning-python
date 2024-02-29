from collections.abc import Iterable

import numpy as np


def is_onedimensional(iterable: Iterable) -> bool:
    try:
        return np.asarray(iterable).ndim == 1
    except (ValueError, TypeError):
        return False
