import os
import pandas as pd
import json
from datetime import date
from ..utils.saveable import Saveable
from .Dataset import DataSet  # Falls dataset.py im gleichen Ordner liegt

class DeviceData(Saveable):
    sensors: list[DataSet] = []

    def __init__(self, sensors: list[DataSet] = None):
        self.sensors = sensors if sensors else []

    def save(self, filepath: str) -> None:
        for sensor in self.sensors:
            sensor.save(filepath)
        print(f"Alle Sensoren gespeichert in: {filepath}")
