import numpy as np

class ComplexArrayHandler(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array, dtype=np.complex128).view(cls)
        return obj

    def __str__(self):
        return str(self.tolist())  # Konvertiere zu einer lesbaren Liste

    def getLength(self):
        return self.shape[0]  # Korrekt für Arrays

    def getPhase(self, k: int):
        return np.angle(self[k])  # Zugriff auf Element k

    def getComplex(self, k: int):
        return np.imag(self[k])  # Zugriff auf imaginären Teil

    def getReal(self, k: int):
        return np.real(self[k])  # Zugriff auf realen Teil

    def getDistance(self, k: int):
        return np.abs(self[k])  # Zugriff auf Betrag
