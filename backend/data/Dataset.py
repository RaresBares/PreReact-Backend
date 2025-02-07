import os
import pandas as pd
from datetime import date
from backend.utils.saveable import Saveable
from backend.utils.windows import windows


class DataSet(Saveable):
    def __init__(
            self,
            dir: str,
            sensorID: str,
            alias: str,
            type: str,
            raw: list[float],
            fft: list[float] = None,
            stfts: list[tuple[windows, list[float]]] = None,
    ):

        self.time = date.today()
        self.sensorID = sensorID
        self.alias = alias
        self.type = type
        self.raw = raw
        self.fft = fft if fft else []
        self.stfts = stfts if stfts else []
        self.path = dir + "/" + sensorID + "_" + "meas" + ".csv"
        # Statistik berechnen
        self.std_dev = self.calculate_std_dev()
        self.peak = self.calculate_peak()
        self.peak_to_peak = self.calculate_peak_to_peak()
        self.median = self.calculate_median()
        self.rms = self.calculate_rms()
        self.shape_factor = self.calculate_shape_factor()
        self.crest_factor = self.calculate_crest_factor()

    def calculate_std_dev(self):
        return pd.Series(self.raw).std() if self.raw else None

    def calculate_peak(self):
        return (max(self.raw), min(self.raw)) if self.raw else None

    def calculate_peak_to_peak(self):
        return max(self.raw) - min(self.raw) if self.raw else None

    def calculate_median(self):
        return pd.Series(self.raw).median() if self.raw else None

    def calculate_rms(self):
        return (sum(x ** 2 for x in self.raw) / len(self.raw)) ** 0.5 if self.raw else None

    def calculate_shape_factor(self):
        return self.rms / abs(sum(self.raw) / len(self.raw)) if self.raw else None

    def calculate_crest_factor(self):
        return max(self.raw) / self.rms if self.raw else None

    def save(self, dir: str) -> None:
        filepath = os.path.join(dir, f"{self.sensorID}_meas.csv")  # Richtiger Pfadaufbau
        os.makedirs(dir, exist_ok=True)  # Erstellt das Verzeichnis korrekt
        if not os.path.exists(filepath):
            os.makedirs(os.path.abspath(os.path.dirname(filepath)), exist_ok=True)

        file_exists = os.path.exists(filepath)

        data = {
            "Path": filepath,
            "Time": self.time.isoformat(),
            "SensorID": self.sensorID,
            "Alias": self.alias,
            "Type": self.type,
            "StdDev": self.std_dev,
            "Peak": str(self.peak),
            "PeakToPeak": self.peak_to_peak,
            "Median": self.median,
            "RMS": self.rms,
            "ShapeFactor": self.shape_factor,
            "CrestFactor": self.crest_factor,
            "Raw": str(self.raw),
            "FFT": str(self.fft),
            "STFTs": str([(str(w), str(f)) for w, f in self.stfts]),
        }

        df = pd.DataFrame([data])
        df.to_csv(filepath, mode="a", header=not file_exists, index=False, sep=";")
        print(f"Verzeichnis existiert: {os.path.exists(dir)}, Pfad: {dir}")
        print(f"DataSet gespeichert unter: {filepath}")


# Proof of Concept
def main():
    dataset = DataSet(
        dir="./dirs",
        sensorID="SENSOR_001",
        alias="MotorVibration",
        type="Vibration",
        raw=[0.1, 0.3, -0.2, 0.5, -0.4, 0.2],
    )
    dataset.save("./dirs")


if __name__ == "__main__":
    main()
