from enum import Enum
from typing import Callable

class Sensortype(Enum):
    Window1 = (1, "Addition")
    FUNCTION_B = (2, "Multiplikation")

    def __init__(self, id: int, name: str, func: Callable):
        self.id = id
        self.name = name



