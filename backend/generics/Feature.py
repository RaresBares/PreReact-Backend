import numpy as np
import json
from enum import Enum
from backend.utils.WeightingFunctions import WeightingFunctions


class Feature(np.ndarray):
    def __new__(cls, values, name="", crest_factor=None, peak_to_peak=None, rms=None, energy=None, std_dev=None, peak=tuple()):
        if not name:
            raise ValueError("Name of VectorFeature cannot be empty")

        obj = np.asarray(values, dtype=np.complex128).view(cls)
        obj._name = name
        obj._crest_factor = crest_factor
        obj._peak_to_peak = peak_to_peak
        obj._rms = rms
        obj._peak = peak
        obj._energy = energy
        obj._std_dev = std_dev



        return obj

    def __str__(self):
        return json.dumps({
            "values": [[float(v.real), float(v.imag)] for v in self.tolist()],
            "type": "vector",
            "name": self._name,
            "crest_factor": [float(self.crest_factor.real), float(self.crest_factor.imag)] if self.crest_factor is not None else "",
            "peak_to_peak": [float(self.peak_to_peak.real), float(self.peak_to_peak.imag)] if self.peak_to_peak is not None else "",
            "rms": [float(self.rms.real), float(self.rms.imag)] if self.rms is not None else "",
            "energy": [float(self.energy.real), float(self.energy.imag)] if self.energy is not None else "",
            "std_dev": [float(self.std_dev.real), float(self.std_dev.imag)] if self.std_dev is not None else ""
        })

    @classmethod
    def from_string(cls, string):
        data = json.loads(string)
        return cls([np.complex128(complex(v[0], v[1])) for v in data["values"]], data["name"],
                   np.complex128(complex(*data["crest_factor"])) if data.get("crest_factor") else None,
                   np.complex128(complex(*data["peak_to_peak"])) if data.get("peak_to_peak") else None,
                   np.complex128(complex(*data["rms"])) if data.get("rms") else None,
                   np.complex128(complex(*data["energy"])) if data.get("energy") else None,
                   np.complex128(complex(*data["std_dev"])) if data.get("std_dev") else None)

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
    def peak(self):
        return self._peak if self._peak is not None else (np.min(self), np.max(self))

    @peak_to_peak.setter
    def peak_to_peak(self, value):

        self._peak = value if value else abs(self.peak[0] - self.peak[1])

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

    def get_squared_copy(self):
        return [x*x for x in self]

    def get_abs_copy(self):
        return [abs(x) for x in self]


    def get_exact_value(self, index, weighting_function=None):
        print(f"{index} of {len(self)}")
        if weighting_function is None:
            return self[index]

        if 0 <= index < len(self):
            if weighting_function:
                return sum(self[i] * weighting_function(i, index) for i in range(len(self)))
            return self[index]
        raise IndexError("Index out of range")

    def get_rounded_copy(self, weight: WeightingFunctions = None,
                         step: int = 1):
        if weight is None:
            weight = WeightingFunctions.GAUSSIAN(abs(self.peak_to_peak)*1.5, 1)

        return [self.get_exact_value(index=i, weighting_function=weight) for i in range(0, len(self), step)]
