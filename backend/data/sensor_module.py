import json
import os
import h5py
import numpy as np
from datetime import date

from pyexpat import features
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable
from backend.generics.Feature import Feature
from backend.utils.STFT import STFT


class Sensor(Saveable):
    def __init__(self, hdf5 : h5py.Group, features : dict[Feature] = None, file: str = None, sensorID: str = "", alias: str = "", sensortype: Sensortype = None, location: str = "",
                 measure_time=None, description=None):

        self.alias = alias
        self.sensortype = Sensortype.get_sensortype_by_name(sensortype)
        self.sensorid = sensorID
        self.features = features

        self.alias = alias
        self.sensortype = Sensortype.get_sensortype_by_name(sensortype)
        self.sensorid = sensorID
        self.measure_time = measure_time
        self.location = location
        self.description = description

        if hdf5 is not None:
            self.alias = hdf5.attrs["alias"]
            self.sensortype = Sensortype.get_sensortype_by_name(hdf5.attrs["sensortype"])
            self.sensorid = hdf5.attrs["sensorid"]
            self.measure_time = hdf5.attrs["measure_time"]
            self.location = hdf5.attrs["location"]
            self.description = hdf5.attrs["description"]
            for table in hdf5.keys():
                if table != "STFTS":
                    dataset = hdf5[table]
                    feature = Feature(values=dataset[:],
                                      name=dataset.attrs["name"],
                                      crest_factor=dataset.attrs["crest_factor"],
                                      std_dev=dataset.attrs["std_dev"],
                                      peak_to_peak=dataset.attrs["peak_to_peak"],
                                      energy=dataset.attrs["energy"],
                                      peak=dataset.attrs["peak"])
                    self.features[dataset.attrs["name"]] = feature


    def __str__(self):
        return f"[ID: {self.sensorID}]"

    def isType(self, type: Sensortype):
        return self.type == type

    def getValues(self):
        return list(self.features.keys()) + list(self.stfts.keys())

    def get_feature(self, feature_name):
        return self.features.get(feature_name, None)

    def get_stft(self, stft_name):
        return self.stfts.get(stft_name, None)

    def save(self, destination : h5py.Group) -> None:
        sensorgroup = destination.create_group(self.sensorid);
        sensorgroup.attrs["sensorid"] = self.sensorid or ""
        sensorgroup.attrs["location"] = self.location or ""
        sensorgroup.attrs["description"] = self.description or ""
        sensorgroup.attrs["alias"] = self.alias or ""
        sensorgroup.attrs["measure_time"] = self.measure_time or ""
        sensorgroup.attrs["sensortype"] = self.sensortype or ""

        for featurekey in self.features.keys():
            feature = self.features[featurekey]
            dataset = sensorgroup.create_dataset(name=feature.name, data=feature)
            dataset.attrs["std_dev"] = feature.std_dev or -1
            dataset.attrs["energy"] = feature.energy or -1
            dataset.attrs["peak_to_peak"] = feature.peak_to_peak or -1
            dataset.attrs["peak"] = feature.peak or (-1,-1)
            dataset.attrs["name"] = feature.name or ""
            dataset.attrs["crest_factor"] = feature.crest_factor or -1
