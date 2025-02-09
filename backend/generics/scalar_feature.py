import numpy as np
import json
from enum import Enum


class ScalarFeature:
    def __init__(self, value, name=""):
        if not name:
            raise ValueError("Name of ScalarFeature cannot be empty")

        self._value = np.complex256(value)
        self._name = name

    def __str__(self):
        return json.dumps({
            "value": str(self._value),
            "name": self._name,
            "magnitude": self.magnitude,
            "squared": self.squared,
            "square_root": self.square_root
        })

    @classmethod
    def from_string(cls, string):
        data = json.loads(string)
        return cls(np.complex256(data["value"]), data["name"])

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def magnitude(self):
        return np.abs(self._value)

    @property
    def squared(self):
        return self._value ** 2

    @property
    def square_root(self):
        return np.sqrt(self._value)

# Example Usage:
# scalar = ScalarFeature(3+4j, name="MyScalar")
# print(scalar.magnitude)
# print(scalar.squared)
# print(scalar.square_root)
# print(scalar.name)
# str_scalar = str(scalar)
# new_scalar = ScalarFeature.from_string(str_scalar)
