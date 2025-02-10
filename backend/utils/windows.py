from typing import Callable
import numpy as np

class WindowFunction:
    def __init__(self, func: Callable[[int, int], float], label: str, window_size: int):
        self.func = func
        self.label = label
        self.window_size = window_size

    def __call__(self, i: int, window_size) -> float:
        if 0 <= i < self.window_size:
            return self.func(i, window_size)
        return 0.0  # Alles außerhalb des Fensters ist 0

    def __str__(self):
        return self.label

# Vordefinierte Fensterfunktionen

def rectangular_window(i: int, window_size: int) -> float:
    return 1.0  # Konstant über das gesamte Fenster

def triangular_window(i: int, window_size: int) -> float:
    return 1 - abs((i - (window_size - 1) / 2) / ((window_size - 1) / 2))

def gaussian_window(i: int, window_size: int, sigma: float = 0.4) -> float:
    return np.exp(-0.5 * ((i - (window_size - 1) / 2) / (sigma * (window_size - 1) / 2)) ** 2)

# Factory-Funktion zur Erstellung einer Fensterfunktion
def create_window_function(type: str, window_size: int) -> WindowFunction:
    windows = {
        "rectangular": WindowFunction(rectangular_window, "Rectangular", window_size),
        "triangular": WindowFunction(triangular_window, "Triangular", window_size),
        "gaussian": WindowFunction(lambda i, w: gaussian_window(i, w), "Gaussian", window_size),
    }
    return windows.get(type.lower(), None)
