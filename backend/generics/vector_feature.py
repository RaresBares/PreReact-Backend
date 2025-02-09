import numpy as np
import json
from enum import Enum
from backend.utils.WeightingFunctions import WeightingFunctions


class VectorFeature(np.ndarray):
    def __new__(cls, values, name="", crest_factor=None, peak_to_peak=None, rms=None, energy=None, std_dev=None):
        if not name:
            raise ValueError("Name of VectorFeature cannot be empty")

        obj = np.asarray(values, dtype=np.complex256).view(cls)
        obj._name = name
        obj._crest_factor = crest_factor
        obj._peak_to_peak = peak_to_peak
        obj._rms = rms
        obj._energy = energy
        obj._std_dev = std_dev
        return obj

    def __str__(self):
        return json.dumps({
            "values": self.tolist(),
            "name": self._name,
            "crest_factor": self.crest_factor,
            "peak_to_peak": self.peak_to_peak,
            "rms": self.rms,
            "energy": self.energy,
            "std_dev": self.std_dev
        })

    @classmethod
    def from_string(cls, string):
        data = json.loads(string)
        return cls(data["values"], data["name"], data.get("crest_factor"), data.get("peak_to_peak"), data.get("rms"),
                   data.get("energy"), data.get("std_dev"))

    @property
    def name(self):
        return self._name

    @property
    def crest_factor(self):
        return self._crest_factor if self._crest_factor is not None else np.max(self) / self.rms if self.rms else None

    @crest_factor.setter
    def crest_factor(self, value):
        self._crest_factor = value

    @property
    def peak_to_peak(self):
        return self._peak_to_peak if self._peak_to_peak is not None else np.ptp(self)

    @peak_to_peak.setter
    def peak_to_peak(self, value):
        self._peak_to_peak = value

    @property
    def rms(self):
        return self._rms if self._rms is not None else np.sqrt(np.mean(self ** 2))

    @rms.setter
    def rms(self, value):
        self._rms = value

    @property
    def energy(self):
        return self._energy if self._energy is not None else np.sum(np.abs(self) ** 2)

    @energy.setter
    def energy(self, value):
        self._energy = value

    @property
    def std_dev(self):
        return self._std_dev if self._std_dev is not None else np.std(self)

    @std_dev.setter
    def std_dev(self, value):
        self._std_dev = value

    def get_exact_value(self, index, weighting_function=None):

        if weighting_function is None:
            return self[index]

        if 0 <= index < len(self):
            if weighting_function:
                return sum(self[i] * weighting_function(i, index) for i in range(len(self)))
            return self[index]
        raise IndexError("Index out of range")

# Example Usage:
# vec = VectorFeature([1+2j, 2+3j, 3+4j], name="MyVector", crest_factor=5.0, energy=10.0)
# print(vec.crest_factor)
# print(vec.peak_to_peak)
# print(vec.name)
# print(vec.energy)
# print(vec.std_dev)
# print(vec.get_exact_value(1))
# print(vec.get_exact_value(1, WeightingFunctions.GAUSSIAN.value(1.0, 1.0)))  # Gaussian weighting
# str_vec = str(vec)
# new_vec = VectorFeature.from_string(str_vec)
