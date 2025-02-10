import h5py

from backend.utils import windows
from backend.utils.SensorType import Sensortype
from backend.utils.saveable import Saveable
from backend.generics.Feature import Feature
from backend.generics.STFT import STFT


class Sensor(Saveable):
    def __init__(self, hdf5: h5py.Group, features: dict[Feature] = None, file: str = None, sensorID: str = "",
                 alias: str = "", sensortype: Sensortype = None, location: str = "",
                 measure_time=None, description=None):

        self.stfts: list[STFT] = []
        self.features = features if features is not None else {}

        self.alias = alias
        self.sensortype = Sensortype.get_sensortype_by_name(sensortype)
        self.sensorid = sensorID
        self.measure_time = measure_time
        self.location = location
        self.description = description

        if hdf5 is not None:
            self.alias = "No Alias" if hdf5.attrs["alias"] == "" else hdf5.attrs["alias"]
            self.sensortype = "No Type" if Sensortype.get_sensortype_by_name(hdf5.attrs["sensortype"]) == "" else Sensortype.get_sensortype_by_name(hdf5.attrs["sensortype"])
            self.sensorid = hdf5.attrs["sensorid"]
            self.measure_time = hdf5.attrs["measure_time"]
            self.location = hdf5.attrs["location"]
            self.description = hdf5.attrs["description"]
            for table in hdf5.keys():
                if table != "stfts":
                    dataset = hdf5[table]
                    feature = Feature(values=dataset[:],
                                      name=dataset.attrs["name"],
                                      crest_factor=dataset.attrs["crest_factor"],
                                      std_dev=dataset.attrs["std_dev"],
                                      peak_to_peak=dataset.attrs["peak_to_peak"],
                                      energy=dataset.attrs["energy"],
                                      peak=dataset.attrs["peak"])
                    self.features[dataset.attrs["name"]] = feature
                else:
                    stftGroup = hdf5[table]
                    for stft_name in stftGroup.keys():
                        dataset = stftGroup[stft_name]  # Dataset aus der Gruppe holen
                        stft_obj = STFT(
                            window_type=str(dataset.attrs.get("window_function", "")),
                        window_size = int(dataset.attrs.get("window_size", 0)),
                        hop_size = int(dataset.attrs.get("hop_size", 0)),
                        id = str(dataset.attrs.get("stft_id", "")),
                        energy = str(dataset.attrs.get("energy", 0)),
                        peak_to_peak = str(dataset.attrs.get("peak_to_peak", 0)),
                        peaks = str(dataset.attrs.get("peaks", [0, 0])),
                        standard_deviation = str(dataset.attrs.get("standart_deviation", 0))
                        )
                        stft_obj.data = dataset[:]  # STFT-Daten setzen
                        self.stfts.append(stft_obj)

    def __str__(self):
        return f"[ID: {self.sensorid}]"

    def isType(self, type: Sensortype):
        return self.sensortype == type

    def getValues(self):
        # Gibt alle Feature-Namen und STFT-IDs zurück
        feature_keys = list(self.features.keys())
        stft_keys = [stft.id for stft in self.stfts]
        return feature_keys + stft_keys

    def get_feature(self, feature_name):
        return self.features.get(feature_name, None)

    def get_stft(self, stft_id):
        # Sucht in der Liste nach einer STFT mit passender ID
        for stft in self.stfts:
            if stft.id == stft_id:
                return stft
        return None

    def add_stft(self, stft_id: str, window_size: int, window_type: str, hop_size: int):
        """
        Erstellt und fügt eine neue STFT hinzu.
        Prüft, ob die stft_id bereits existiert – falls ja, wird abgebrochen.
        """
        # Überprüfe, ob bereits eine STFT mit der gleichen ID existiert
        if any(stft.id == stft_id for stft in self.stfts):
            print(f"STFT with ID '{stft_id}' already exists. Aborting addition.")
            return

        new_stft = STFT(window_type=window_type, window_size=window_size, hop_size=hop_size, id=stft_id)
        self.stfts.append(new_stft)

    def remove_stft(self, stft_id: str):
        """
        Entfernt die STFT mit der angegebenen ID.
        Falls keine passende STFT gefunden wird, wird ein Fehler ausgelöst.
        """
        for i, stft in enumerate(self.stfts):
            if stft.id == stft_id:
                del self.stfts[i]
                return
        raise ValueError(f"Keine STFT mit ID {stft_id} gefunden.")

    def compute_stft(self):
        """
        Berechnet für alle gespeicherten STFTs den STFT-Wert.
        Hier wird davon ausgegangen, dass das RAW-Signal als Feature unter "RAW" gespeichert ist.
        """
        raw_feature = self.get_feature("RAW")
        if raw_feature is None:
            raise ValueError("Das Feature 'RAW' wurde nicht gefunden.")
        # Annahme: Das RAW-Signal befindet sich in raw_feature.values.
        for stft in self.stfts:
            stft.compute_stft(raw=raw_feature.values)

    def save(self, destination: h5py.Group) -> None:
        sensorgroup = destination.create_group(self.sensorid)
        sensorgroup.attrs["sensorid"] = self.sensorid or ""
        sensorgroup.attrs["location"] = self.location or ""
        sensorgroup.attrs["description"] = self.description or ""
        sensorgroup.attrs["alias"] = self.alias or ""
        sensorgroup.attrs["measure_time"] = self.measure_time or ""
        sensorgroup.attrs["sensortype"] =  self.sensortype

        for featurekey in self.features.keys():
            feature = self.features[featurekey]
            dataset = sensorgroup.create_dataset(name=feature.name, data=feature)
            dataset.attrs["std_dev"] = feature.std_dev or -1
            dataset.attrs["energy"] = feature.energy or -1
            dataset.attrs["peak_to_peak"] = feature.peak_to_peak or -1
            dataset.attrs["peak"] = feature.peak.tolist() if feature.peak is not None else [-1, -1]
            dataset.attrs["name"] = feature.name or ""
            dataset.attrs["crest_factor"] = feature.crest_factor or -1

        stftgroup = sensorgroup.create_group(name="stfts")
        for stft in self.stfts:
            dataset = stftgroup.create_dataset(stft.id, data=stft.data)
            dataset.attrs["stft_id"] = stft.id
            dataset.attrs["energy"] = str(stft.energy if stft.energy is not None else 0)
            dataset.attrs["standart_deviation"] = str(
                stft.standard_deviation if stft.standard_deviation is not None else 0)
            dataset.attrs["peaks"] = str(stft.peaks if stft.peaks is not None else [0, 0])
            dataset.attrs["peak_to_peak"] = str(stft.peak_to_peak if stft.peak_to_peak is not None else 0)
            dataset.attrs["window_function"] = str(stft.window_function)
            dataset.attrs["hop_size"] = str(stft.hop_size if stft.hop_size is not None else 0)
            dataset.attrs["window_size"] = str(stft.window_size if stft.window_size is not None else 0)

