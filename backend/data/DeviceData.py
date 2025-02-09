import os
import pandas as pd
import json
from datetime import date
from tabulate import tabulate
import yaml as yaml
from numpy.ma.core import append

from backend.data.Dataset import DataSet
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable

# returns array of DataSets of Sensors listed in map.yaml in dir
def loadSensorsFromYaml(dir):
    file = os.path.join(dir, "map.yaml")
    if os.path.exists(file):
        with (open(file, 'r') as f):
            map = yaml.load(f, Loader=yaml.FullLoader)
            sensors : list(DataSet) = []
            for i in range(0, len(map["sensors"])):
                sensorInfo = map["sensors"][i]
                path = os.path.join(dir, sensorInfo[list(sensorInfo.keys())[0]]["file_location"], sensorInfo[list(sensorInfo.keys())[0]]["sensorid"] + "_meas.csv")
                sensor = DataSet(path)
                sensor.loadFromFile( info=sensorInfo[list(sensorInfo.keys())[0]], super_info=map["super_info"])
                sensors.append(sensor)
            return sensors
    else:
        print(f"{file} doesn't exist. Creating it now. ")
        data = {"sensors": [{"TestSensorID": {"sensorID": "/"}}]}
        with open(file, 'w') as f:
            yaml.dump(data, f)
            print(f"{file} created!")
        return []

class DeviceData(Saveable):
    sensors: list[DataSet] = []

    def count_sensors(self):
        return len(self.sensors)

    def get_sensors(self):
        return self.sensors

    def get_sensor_by_id(self, id: str):
        for sensor in self.sensors:
            if sensor.sensorID == id:
                return sensor
            else:
                None
    def get_sensors_by_type(self, type:Sensortype):
        result_list = [];
        for sensor in self.sensors:
            if(sensor.isType(type)):
                result_list.append(sensor)
        return result_list

    def getLocation(self):
        return self.dir

    def getDate(self):
        return

    def yamlExists(self):
        return os.path.exists(os.path.join(dir, "map.yaml"))

    def getYaml(self):
        if self.yamlExists():
            with open(os.path.join(dir, "map.yaml")) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            return None

    def getInfo(self, info:str):
        return self.getYaml()[info]

    def __init__(self, sensors: list[DataSet] = None, dir : str = None):
        self.sensors = sensors if sensors else []
        self.dir = dir;
        if(not sensors == [] and os.path.exists(dir)):
           self.sensors =  loadSensorsFromYaml(dir)
        else:
            print("Error! Directory doesn't exist!")




    def save(self, dir: str = dir) -> None:
        for sensor in self.sensors:
            sensor.save(dir=dir)
        print(f"{len(self.sensors)} sensors saved in: {dir}")

    def introduce(self):

        data = [];

        for sensor in self.sensors:
            data.append([sensor.alias, sensor.sensorID, sensor.type, sensor.location])

        headers = ["Alias", "SensorID", "SensorType", "Location"]

        print(tabulate(data, headers, tablefmt="grid"))

if __name__ == "__main__":
    device = DeviceData(dir="./measurement")
    device.introduce()
    i = 0
    for sensor in device.sensors:
        i = i + 1;
        sensor.stfts[1][1][0] = 2 + 4j;
        device.save("./savetest");
        print(f"{i}er Sensor: {sensor.type}")
        sensor.update_scalars()
##        print(str([float(round(x.real, 2)) + float(round(x.imag, 2)) * 1j for x in sensor.stfts[1][1]]))
