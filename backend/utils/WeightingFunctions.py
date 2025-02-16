from enum import Enum

import numpy as np


class WeightingFunctions(Enum):
    GAUSSIAN = staticmethod(
        lambda std_dev, max_val: (lambda i, j: max_val * np.exp(-((i - j) ** 2) / (2 * std_dev ** 2))))
    RECTANGLE = staticmethod(lambda width, height: (lambda i, j: height if abs(i - j) <= width / 2 else 0))
    TRIANGLE = staticmethod(
        lambda width, height: (lambda i, j: height * (1 - abs(i - j) / (width / 2)) if abs(i - j) <= width / 2 else 0))
    EXPONENTIAL = staticmethod(lambda decay: (lambda i, j: np.exp(-decay * abs(i - j))))
    LINEAR_DECAY = staticmethod(lambda max_val, slope: (lambda i, j: max(0, max_val - slope * abs(i - j))))
    DELTA = lambda i, j: 1 if i == j else 0
