import numpy as np
from typing import Iterable


def lp(x: Iterable[float], y: Iterable[float], p: float, axis=None) -> float:
    """
    normalized to [0, 0.5]
    x and y are expected to be unit vectors
    """
    return np.linalg.norm(x-y, ord=p, axis=axis) / 4


def l1(x, y, axis=None):
    return lp(x, y, 1, axis=axis)


def l2(x, y, axis=None):
    return lp(x, y, 2, axis=axis)


distance = l2
