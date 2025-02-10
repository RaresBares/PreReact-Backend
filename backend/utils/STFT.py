from typing import Callable
import numpy as np
import json

from backend.utils.windows import windows


class STFT:
    def __init__(self, window: windows, name: str = ""):
        if not name:
            raise ValueError("STFT must have a name")
        self.window = window
        self.stft = np.array([], dtype=np.complex256)  # Initialisiert als leeres Array
        self.name = name

    def compute_stft(self, raw: np.ndarray, window_size: int, hop_size: int, omega: np.ndarray):
        """
        Berechnet die diskrete STFT eines Signals.

        :param raw: Eingangs-Signal als numpy Array
        :param window_size: Länge des Fensters (Anzahl der Samples pro Segment)
        :param hop_size: Schrittweite zwischen den Fenstern (Überschneidung)
        :param omega: Frequenzachsen-Werte
        """
        n = len(raw)
        self.stft = []  # Liste für die STFT-Werte

        for m in range(0, n - window_size + 1, hop_size):
            segment = raw[m:m + window_size]  # Fenstersegment
            windowed_segment = np.array(
                [x * self.window.func(i, window_size) for i, x in enumerate(segment)],
                dtype=np.complex256)  # Fensterung
            stft_m = np.array(
                [sum(windowed_segment * np.exp(-1j * w * np.arange(len(segment), dtype=np.complex256))) for w in omega],
                dtype=np.complex256)
            self.stft.append(stft_m)

        self.stft = np.array(self.stft, dtype=np.complex256)
        return self.stft

    def get_stft_value(self, m: int, omega_idx: int):
        """
        Gibt den STFT-Wert für ein bestimmtes Offset m und eine bestimmte Frequenz omega zurück.

        :param m: Index des Offsets (Fensterposition)
        :param omega_idx: Index der Frequenzkomponente
        :return: Komplexer STFT-Wert
        """
        if 0 <= m < len(self.stft) and 0 <= omega_idx < len(self.stft[m]):
            return self.stft[m, omega_idx]
        else:
            raise ValueError("Ungültiger Index für m oder omega.")

    def get_max_m(self):
        """
        Gibt den maximalen Wert für m (die Anzahl der Fenster) zurück.
        """
        return len(self.stft) - 1 if self.stft.size > 0 else None

    def get_max_omega(self):
        """
        Gibt den maximalen Index für omega (die Anzahl der Frequenzkomponenten) zurück.
        """
        return len(self.stft[0]) - 1 if self.stft.size > 0 else None

    def __str__(self):
        return json.dumps({
            "name": self.name,
            "type": "stft",
            "window": str(self.window),
            "stft": [[str(x) for x in row.tolist()] for row in self.stft]
        })

    @classmethod
    def from_string(cls, string):
        data = json.loads(string)
        obj = cls(
            window=data["window"],
            name=data["name"]
        )
        obj.stft = np.array([[np.complex256(x) for x in row] for row in data["stft"]], dtype=np.complex256)
        return obj