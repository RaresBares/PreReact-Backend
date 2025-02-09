from typing import Callable
import numpy as np

from backend.utils.windows import windows


class STFT:

    def __init__(self, window: windows, raw: list[np.complex128]):
        self.window = window
        self.raw = raw
        self.stft = []  # Initialisiert als leere Liste

    def compute_stft(self, window_size: int, hop_size: int, omega: np.ndarray):
        """
        Berechnet die diskrete STFT eines Signals.

        :param window_size: Länge des Fensters (Anzahl der Samples pro Segment)
        :param hop_size: Schrittweite zwischen den Fenstern (Überschneidung)
        :param omega: Frequenzachsen-Werte
        """
        n = len(self.raw)
        self.stft = []  # Liste für die STFT-Werte

        for m in range(0, n - window_size + 1, hop_size):
            segment = self.raw[m:m + window_size]  # Fenstersegment
            windowed_segment = np.array(
                [x * self.window.func(i, window_size) for i, x in enumerate(segment)])  # Fensterung
            stft_m = [sum(windowed_segment * np.exp(-1j * w * np.arange(len(segment)))) for w in omega]
            self.stft.append(stft_m)

        return self.stft

    def get_stft_value(self, m: int, omega_idx: int):
        """
        Gibt den STFT-Wert für ein bestimmtes Offset m und eine bestimmte Frequenz omega zurück.

        :param m: Index des Offsets (Fensterposition)
        :param omega_idx: Index der Frequenzkomponente
        :return: Komplexer STFT-Wert
        """
        if 0 <= m < len(self.stft) and 0 <= omega_idx < len(self.stft[m]):
            return self.stft[m][omega_idx]
        else:
            raise ValueError("Ungültiger Index für m oder omega.")

    def get_max_m(self):
        """
        Gibt den maximalen Wert für m (die Anzahl der Fenster) zurück.
        """
        return len(self.stft) - 1 if self.stft else None

    def get_max_omega(self):
        """
        Gibt den maximalen Index für omega (die Anzahl der Frequenzkomponenten) zurück.
        """
        return len(self.stft[0]) - 1 if self.stft else None
