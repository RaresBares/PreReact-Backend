from enum import Enum
from typing import Callable

class windows(Enum):
    Window1 = (1, "Addition", lambda x, y: x + y)
    FUNCTION_B = (2, "Multiplikation", lambda x, y: x * y)

    def __new__(cls, id: int, label: str, func: Callable):
        obj = object.__new__(cls)
        obj._value_ = id  # Setze den Enum-Wert
        obj.label = label  # Benutzerdefiniertes Attribut
        obj.func = func  # Funktion speichern
        return obj


