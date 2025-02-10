import os
import h5py
import json
from datetime import date
from tabulate import tabulate

from backend.data.sensor_module import Sensor
from backend.generics.Feature import Feature
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable

class DeviceData(Saveable):
    def __init__(self, sensors : list[Sensor], file_path  : str =""):
        self.sensors = sensors or []
        self.file_path = file_path
        if os.path.exists(file_path):
            self.load_sensors_from_hdf5()
        else:
            print("HDF5 file does not exist!")


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
                sensor.save(f)

    def introduce(self):
        data = [[sensor.alias, sensor.sensorID, sensor.type] for sensor in self.sensors]
        headers = ["Alias", "SensorID", "SensorType"]
        print(tabulate(data, headers, tablefmt="grid"))



sensor1 = Sensor(hdf5=None, sensorID="sensor001", alias="First", sensortype=Sensortype.MICROPHONE, features={

    "Raw" : Feature([1,2,3,4,5,6], name="Raw")

})

sensor2 = Sensor(hdf5=None, sensorID="sensor002", alias="First", sensortype=Sensortype.MICROPHONE, features={

    "Raw" : Feature([1,2,3,4,5,6], name="Raw"),
    "FFT" : Feature([1,0,1,0,1,0,2,9], name="FFT")

})

device = DeviceData([sensor1,sensor2])
device.save("./save.h5")
