import os
import pandas as pd
import json
from datetime import date

import yaml as yaml

from backend.utils.saveable import Saveable
from Dataset import DataSet  # Falls dataset.py im gleichen Ordner liegt


def loadFromDirectonary(dir):
    with open(os.path.join(dir, "map.yaml"), 'r') as f:
        map = yaml.load(f, Loader=yaml.FullLoader)
        for sens in map["sensors"]:
            sensorInfo = map["sensors"][sens]
            sensor = DataSet(sensorInfo["sensorID"], dir)


class DeviceData(Saveable):
    sensors: list[DataSet] = []

    def __init__(self, sensors: list[DataSet] = None, dir : str = None):
        self.sensors = sensors if sensors else []

        if(not sensors and os.path.exists(dir)):
            loadFromDirectonary(dir)
        else:
            print("Error! Directory doesn't exist!")




    def save(self, filepath: str) -> None:
        for sensor in self.sensors:
            sensor.save(filepath)
        print(f"Alle Sensoren gespeichert in: {filepath}")


if __name__ == "__main__":
    dataset = DataSet("./dat/SENSOR_001_meas.csv")
    dataset.load("./dat/SENSOR_001_meas.csv")
    dataset.raw = [1, 0, 1, 0, 1, 0]
    dataset.calculate_fft()
    dataset.calculate_stft()
    dataset.alias = dataset.alias + "test"
    dataset.save("./dat")
    print("Test: " + str([round(x.real, 2) + round(x.imag, 2) * 1j for x in dataset.fft]))