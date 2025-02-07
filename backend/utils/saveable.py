from abc import ABC, abstractmethod

class Saveable(ABC):
    """Interface für Klassen, die speicherbar sein sollen."""

    @abstractmethod
    def save(self, filepath: str) -> None:
        """Speichert die Daten in eine Datei."""
        pass
