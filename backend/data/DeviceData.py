import os
import h5py
import json
from datetime import date

import numpy as np
from tabulate import tabulate

from backend.data.sensor_module import Sensor
from backend.generics.Feature import Feature
from backend.generics.STFT import STFT
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable
import backend.utils.windows


class DeviceData(Saveable):
    def __init__(self, sensors : list[Sensor], file_path  : str =""):
        self.sensors = sensors or []
        self.file_path = file_path


    @classmethod
    def load_sensors_from_hdf5(self, file_path : str=None):
        sensors = {}
        with h5py.File(file_path, "r") as f:
            for sensorid in f.keys():
                sensor_group = f[sensorid]
                sensor = Sensor(hdf5 = sensor_group)
                sensors[sensorid] = sensor
        return DeviceData(sensors=sensors, file_path=file_path)


    def count_sensors(self):
        return len(self.sensors)

    def get_sensors(self):
        return self.sensors

    def get_sensor_by_id(self, sensor_id):
        return next((sensor for sensor in self.sensors if sensor.sensorID == sensor_id), None)

    def get_sensors_by_type(self, sensor_type):
        return [sensor for sensor in self.sensors if sensor.isType(sensor_type)]

    def save(self, file_path):
        with h5py.File(file_path, "w") as f:
            for sensor in self.sensors:
                self.sensors[sensor].save(f)

    def introduce(self):
        data = [[self.sensors[sensor].alias, self.sensors[sensor].sensorid, self.sensors[sensor].sensortype] for sensor in self.sensors]
        headers = ["Alias", "SensorID", "SensorType"]
        print(tabulate(data, headers, tablefmt="grid"))


'''
# Erstelle ein Test-Signal mit 1024 Samples, das jede Viertelsekunde die Frequenz ändert
fs = 10_000  # Abtastrate
n = 10_000  # Länge des Signals

t = np.arange(n) / fs

# Vier verschiedene Frequenzen für je 256 Samples
raw_signal = np.concatenate([
    np.sin(2 * np.pi * 10 * t[:2500]),
    np.sin(2 * np.pi * 20 * t[2500:5000]),
    np.sin(2 * np.pi * 40 * t[5000:7500]),
    np.sin(2 * np.pi * 80 * t[10_000:])
])

device = DeviceData.load_sensors_from_hdf5("./save.h5")
a = STFT(window_type="blackman", window_size=100, hop_size=10, id="blackman", data=device.sensors["sensor001"].get_feature("Raw"));
a.compute_stft(device.sensors["sensor001"].get_feature("Raw"))
device.sensors["sensor001"].stfts.append(a)



device.save("./save2.h5")

print("Proof of Concept erfolgreich abgeschlossen. STFT-Daten gespeichert.")
'''