import json
import os
import pandas as pd
from datetime import date
import tqdm
import time
from backend.utils.ComplexArrayHandler import ComplexArrayHandler
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable
from backend.utils.windows import windows
import numpy as np
import ast
from tabulate import tabulate


class DataSet(Saveable):

    def __init__(
            self,
            path:str = None,
            dir: str = None,
            sensorID: str= "",
            alias: str= "",
            sensortype: Sensortype= None,
            raw: list[float]= None,
            fft: list[float] = None,
            stfts: list[tuple[windows, list[float]]] = None,
            location:str = ""
    ):
        self.measure_time = None
        self.measure_date = None
        self.measure_timestamp = None
        self.location = location
        self.time = date.today()
        self.sensorID = sensorID
        self.alias = alias
        self.type = sensortype
        self.raw = np.array(raw)
        self.fft = fft if fft else []
        self.fft = np.array(fft) if fft else []
        self.stfts = stfts if stfts else []
        if (dir is not None) and (sensorID is not None):
            self.path = os.path.join(dir, sensorID + "_meas.csv")
        else:
            if path is not None:
                self.path = path
            else:
                raise ValueError("Path, Dir and sessionid not set")
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

    def update_all(self):
         if self.raw:
            print("Update values...")
            with tqdm(total=1, desc="FFT-Berechnung", unit=" steps") as pbar:
                self.update_scalars()
                pbar.update(0.4)
                self.calculate_fft()
                pbar.update(0.8)
                self.calculate_stft()
                pbar.update(1)


    def save(self, dir: str) -> None:
            filepath = os.path.join(dir, f"{self.sensorID}_meas.csv")  # Richtiger Pfadaufbau
            os.makedirs(dir, exist_ok=True)  # Erstellt das Verzeichnis korrekt
            if not os.path.exists(filepath):
                os.makedirs(os.path.abspath(os.path.dirname(filepath)), exist_ok=True)

            file_exists = os.path.exists(filepath)

            data = {
                "Path": filepath,
                "description": self.description,
                "location": self.location,
                "measure_date": self.measure_date,
                "measure_time": self.measure_time,
                "measure_timestamp": self.measure_timestamp,
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

    def loadFromFile(self, info=None, super_info=None) -> None:
        if super_info is None:
            super_info = {}
        if info is None:
            info = {}
        if not os.path.exists(self.path):
            print(f"Datei {self.path} existiert nicht.")
            return

        self.measure_date = super_info.get("measure_date")
        self.measure_time = super_info.get("measure_time")
        self.measure_timestamp = super_info.get("measure_timestamp")

        df = pd.read_csv(self.path, sep=";")

        for _, row in df.iterrows():

            self.sensorID = info.get("sensorid") or row["sensorid"]
            self.location = info.get("sensor_location") or row["location"]
            self.description = info.get("description") or row["description"]
            self.alias = info.get("alias") or row["alias"]
            self.type = Sensortype.get_sensortype_by_name(info.get("sensortype") or row["sensortype"]);
            self.raw= np.array(ast.literal_eval(row["RAW"])).tolist();
            self.fft = ComplexArrayHandler(np.array(ast.literal_eval(row["FFT"])));
            self.stfts=[[a, ComplexArrayHandler(ast.literal_eval(s))] for a, s in ast.literal_eval(row["STFTs"])]




