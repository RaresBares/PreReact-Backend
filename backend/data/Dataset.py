import json
import os
import pandas as pd
from datetime import date

from backend.utils.ComplexArrayHandler import ComplexArrayHandler
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable
from backend.utils.windows import windows
import numpy as np
import ast

class DataSet(Saveable):

    def __init__(
            self,
            dir: str = None,
            sensorID: str= "",
            alias: str= "",
            sensortype: Sensortype= None,
            raw: list[float]= None,
            fft: list[float] = None,
            stfts: list[tuple[windows, list[float]]] = None,
    ):

        self.time = date.today()
        self.sensorID = sensorID
        self.alias = alias
        self.type = sensortype
        self.raw = np.array(raw)
        self.fft = fft if fft else []
        self.fft = np.array(fft) if fft else []
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

    def __str__(self):
        return f"[ID: {self.sensorID}]"

    def isType(self, type : Sensortype):
        if self.type == type:
            return True;
        return False;

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

    def calculate_fft(self):
        if self.raw:
            fft_result = np.fft.fft(self.raw)
            self.fft = ComplexArrayHandler(fft_result)

    def calculate_stft(self):
        self.stfts = [(w, np.abs(np.fft.fft([w.func(x, 0) for x in self.raw])).tolist()) for w in windows]

    def update_stft(self):
        self.stfts = [(w, np.abs(np.fft.fft([w.func(x, 0) for x in self.raw])).tolist()) for w in windows]

    def update_scalars(self):
        self.rms = self.calculate_rms();
        self.peak = self.calculate_peak()
        self.peak_to_peak = self.calculate_peak_to_peak()

    def save(self, dir: str) -> None:
        filepath = os.path.join(dir, f"{self.sensorID}_meas.csv")  # Richtiger Pfadaufbau
        os.makedirs(dir, exist_ok=True)  # Erstellt das Verzeichnis korrekt
        if not os.path.exists(filepath):
            os.makedirs(os.path.abspath(os.path.dirname(filepath)), exist_ok=True)

        file_exists = os.path.exists(filepath)

        data = {
            "Path": filepath,
            "Date": self.time.isoformat(),
            "Time": self.time.isoformat(),
            "TimeStamp": self.time.isoformat(),
            "SensorID": self.sensorID,
            "Alias": self.alias,
            "Type": self.type.name,
            "StdDev": self.std_dev,
            "Peak": str(self.peak),
            "PeakToPeak": self.peak_to_peak,
            "Median": self.median,
            "RMS": self.rms,
            "ShapeFactor": self.shape_factor,
            "CrestFactor": self.crest_factor,
            "RAW": self.raw,
            "FFT": str(self.fft),
            "STFTs": str([(str(w), str(f)) for w, f in self.stfts]),
        }
        df = pd.DataFrame([data])
        df.to_csv(filepath, mode="w", header=True, index=False, sep=";")
        print(f"Verzeichnis existiert: {os.path.exists(dir)}, Pfad: {dir}")
        print(f"DataSet gespeichert unter: {filepath}")

    def loadFromFile(dir: str, alias:str = "NoAlias", sensorID : str = None, sensortype: Sensortype | str = None):
        if isinstance(sensortype, str):
            sensortype = Sensortype.get_sensortype_by_name(sensortype);

        sensor = DataSet(dir=dir, sensorID=sensorID, sensortype=sensortype);
        sensor.load(alias=alias, path=os.path.join(dir, sensorID + "_meas.csv"), sensorID=sensorID, sensortype=sensortype);
        return sensor

    def load(self, alias:str,  path: str = "", sensorID : str = None, sensortype:Sensortype|str = None) -> None:
        if isinstance(sensortype, str):
            sensortype = Sensortype.get_sensortype_by_name(sensortype);

        if not os.path.exists(path):
            print(f"Datei {path} existiert nicht.")
            return

        df = pd.read_csv(path, sep=";")

        for _, row in df.iterrows():
            self.dir=os.path.dirname(path)
            if not sensorID:
                self.sensorID= row["SensorID"]
            else:
                self.sensorID=sensorID

            if alias:
                self.alias = alias
            else:
                self.alias= row["Alias"]


            if sensortype:
                self.type = sensortype;
            else:
                Sensortype.get_sensortype_by_name(row["Type"])
            self.raw= np.array(ast.literal_eval(row["RAW"])).tolist();
            self.fft = ComplexArrayHandler(np.array(ast.literal_eval(row["FFT"])));
            self.stfts=[[a, ComplexArrayHandler(ast.literal_eval(s))] for a, s in ast.literal_eval(row["STFTs"])]





