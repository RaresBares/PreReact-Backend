import numpy as np
from backend.data.DeviceData import DeviceData
from backend.data.sensor_module import Sensor


class Importer:
    @staticmethod
    def import_sensorlist_from_file(source_file, force_accelerators=True):
        """
        Lädt Sensordaten aus einer .npy-Datei und erstellt Sensor-Objekte.

        Die .npy-Datei enthält ein Array, bei dem:
          - Jede Zeile (erste Dimension) ein Vektor mit den Messwerten an einer bestimmten Position ist.
          - Jeder Sensor durch die Werte an einem Index in diesen Vektoren repräsentiert wird.
          Beispiel: source_array[0][3] ist der 1. Messwert (erste Zeile) des 4. Sensors.

        Wir transponieren das Array, sodass jeder Sensor seinen eigenen Datenvektor erhält.

        :param source_file: Pfad zur .npy-Datei.
        :param force_accelerators: Wenn True, erhalten alle Sensoren automatisch
                                   eine ID im Format "sensorXXX" und den Typ "ACCELERATOR".
                                   Andernfalls wird einmalig vom Benutzer abgefragt,
                                   wobei für jeden Sensor eine individuelle ID generiert wird.
        :return: Dictionary, in dem die Keys die SensorIDs und die Values die Sensor-Objekte sind.
        """
        # Laden des numpy-Arrays
        raw_data = np.load(source_file, "r")
        # raw_data hat die Form (num_components, num_sensors)
        # Transponieren, sodass jeder Sensor seinen eigenen Messwerte-Vektor erhält:
        sensors_data = raw_data.T  # neue Form: (num_sensors, num_components)

        sensors = {}  # Dictionary: SensorID --> Sensor
        if force_accelerators:
            # Automatische Vergabe: IDs im Format sensor000, sensor001, etc. und Typ "ACCELERATOR"
            for idx, data in enumerate(sensors_data):
                sensor_id = f"sensor{idx:03d}"  # 3-stellige Nummerierung
                sensor_type = "ACCELERATOR"
                sensor_obj = Sensor(sensorID=sensor_id, sensortype=sensor_type)
                sensor_obj.set_raw(data)
                sensors[sensor_id] = sensor_obj
        else:
            # Einmalige Abfrage der Basis-Sensor-ID und des Sensortyps (z.B. "MICROPHONE" oder "ACCELERATOR")
            base_sensor_id = input("Gib den Basis-Sensor-ID ein (z.B. 'sensor'): ")
            user_sensor_type = input("Gib den Sensortyp ein (MICROPHONE oder ACCELERATOR): ")
            for idx, data in enumerate(sensors_data):
                # Erzeuge eine individuelle Sensor-ID, z.B. sensor000, sensor001, etc., basierend auf der Eingabe
                sensor_id = f"{base_sensor_id}{idx:03d}"
                sensor_obj = Sensor(sensorID=sensor_id, sensortype=user_sensor_type)
                sensor_obj.set_raw(data)
                sensors[sensor_id] = sensor_obj

        return sensors

    @staticmethod
    def import_device_from_npy(source_file: str):
        return DeviceData(sensors=Importer.import_sensorlist_from_file(source_file))


if __name__ == '__main__':
    # Beispielaufruf: force_accelerators True: alle Sensoren werden automatisch als ACCELERATOR erzeugt,
    # und ihre IDs werden als sensor000, sensor001, ... vergeben.
    device = Importer.import_device_from_npy(source_file="../dummy/test.npy")

    # Optional: Ausgabe der erstellten Sensoren zur Kontrolle (Annahme: DeviceData erwartet ein Dictionary)
    for sensor_id, sensor in device.sensors.items():
        print(f"Sensor ID: {sensor_id}, Typ: {sensor.sensortype}")
