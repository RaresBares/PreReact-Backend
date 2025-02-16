import numpy as np
from backend.utils.windows import create_window_function

class STFT:
    def __init__(self, window_type: str, window_size: int, hop_size: int, id: str = "", data=None,
                 energy=None, standard_deviation=None, peaks=None, peak_to_peak=None):
        self.id = id
        self.window_function = create_window_function(window_type, window_size)
        self.window_size = window_size
        self.hop_size = hop_size
        self.data = data
        self.omega = 2 * np.pi * np.arange(window_size // 2 + 1) / window_size  # Nur positive Frequenzen

        # Zusätzliche Metriken als Eigenschaften – entweder über den Konstruktor gesetzt oder später berechnet.
        self.energy = energy
        self.standard_deviation = standard_deviation
        self.peaks = peaks
        self.peak_to_peak = peak_to_peak

    def compute_stft(self, raw: np.ndarray):
        n = len(raw)
        num_frames = max((n - self.window_size) // self.hop_size + 1, 0)
        self.data = np.zeros((num_frames, len(self.omega)), dtype=np.complex128)

        # Fensterwerte einmalig berechnen
        window_values = np.array([self.window_function(i, self.window_size) for i in range(self.window_size)])
        for m in range(num_frames):
            start = m * self.hop_size
            segment = raw[start:start + self.window_size]
            windowed_segment = segment * window_values
            fft_result = np.fft.fft(windowed_segment)[:len(self.omega)]
            self.data[m] = fft_result
        return self.data

    def re_evaluate(self, raw=None):
        """
        Berechnet neu:
          - STFT (wenn raw übergeben wird)
          - Energie, Standardabweichung, Peak-to-Peak und die zwei höchsten Peaks
        """
        if raw is not None:
            self.compute_stft(raw)
        if self.data is None:
            raise ValueError("STFT-Daten wurden noch nicht berechnet.")

        magnitude = np.abs(self.data)
        self.energy = np.sum(magnitude ** 2)  # E = Σ|X(m, ω)|²
        self.standard_deviation = np.std(magnitude)
        self.peak_to_peak = np.max(magnitude) - np.min(magnitude)
        indices = np.unravel_index(np.argsort(magnitude, axis=None)[-2:], magnitude.shape)
        self.peaks = list(zip(indices[0], indices[1]))

    def get_value(self, m: int, omega_idx: int):
        if self.data is None:
            raise ValueError("STFT-Daten wurden noch nicht berechnet.")
        if not (0 <= m < self.data.shape[0]) or not (0 <= omega_idx < self.data.shape[1]):
            raise IndexError("Index außerhalb der gültigen Werte.")
        return self.data[m, omega_idx]

    def get_maximum_frequency(self):
        return max(self.omega) if len(self.omega) > 0 else None

    def get_minimum_frequency(self):
        return min(self.omega) if len(self.omega) > 0 else None

    def get_effective_frequency(self, omega_idx: int):
        if not (0 <= omega_idx < len(self.omega)):
            raise IndexError("Index außerhalb der gültigen Werte.")
        return self.omega[omega_idx]
