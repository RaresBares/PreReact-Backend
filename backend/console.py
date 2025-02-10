import cmd
import os
from backend.data.DeviceData import DeviceData
from backend.utils.SensorType import Sensortype

class SensorConsole(cmd.Cmd):
    prompt = ">>> "  # User prompt
    intro = "Welcome to the Sensor Data Console! Options: load, convert, select, save, etc."

    def __init__(self):
        super().__init__()
        self.device = None
        self.selected_sensor = None

    def do_load(self, arg):
        """Load sensor data from a directory. Syntax: load <directory_path>"""
        if not arg:
            print("Please specify a directory.")
            return

        if not os.path.exists(arg):
            print(f"Directory {arg} does not exist!")
            return

        self.device = DeviceData.load_sensors_from_hdf5(file_path=arg)
        print(f"{len(self.device.sensors)} sensors loaded!")
        print("You can now use commands like 'introduce', 'save', or 'select <sensor_id>'.")

    def do_convert(self, arg):
        """Convert a file (Placeholder)."""
        print("File conversion is not implemented yet.")

    def do_exit(self, arg):
        """Exit the console."""
        print("Goodbye!")
        return True

    def do_introduce(self, arg):
        """Execute DeviceData.introduce() method."""
        if not self.device:
            print("No device loaded. Use 'load <directory>' first.")
            return
        self.device.introduce()

    def do_save(self, arg):
        """Save all sensor data to a directory. Syntax: save <directory>"""
        if not self.device:
            print("No device loaded. Use 'load <directory>' first.")
            return

        if not arg:
            print("Please specify a directory.")
            return

        self.device.save(arg)
        print(f"Data saved to {arg}.")

    def do_select(self, arg):
        """Select a sensor by ID. Syntax: select <sensor_id>"""
        if not self.device:
            print("No device loaded. Use 'load <directory>' first.")
            return

        # Annahme: self.device.sensors ist ein dict: sensorid -> sensor
        if arg in self.device.sensors:
            self.selected_sensor = self.device.sensors[arg]
            print(f"Sensor {arg} selected. Available commands: getValue, setValue, list_features, list_stfts, add_stft, remove_stft, revaluate_stft, revaluate_all, print_sensor.")
        else:
            print(f"Sensor {arg} not found.")

    def do_getValue(self, arg):
        """Retrieve a variable from the selected sensor. Syntax: getValue <variable_name>"""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return

        value = self.selected_sensor.get_feature(arg)
        if value is not None:
            print(f"{arg}: {value}")
        else:
            print(f"Variable '{arg}' does not exist in the selected sensor.")

    def do_setValue(self, arg):
        """Set a variable in the selected sensor. Syntax: setValue <variable_name> <value>"""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return

        parts = arg.split(" ", 1)
        if len(parts) < 2:
            print("Usage: setValue <variable_name> <value>")
            return

        variable_name, value = parts
        try:
            # ACHTUNG: eval() birgt Sicherheitsrisiken!
            self.selected_sensor.features[variable_name] = eval(value)
            print(f"{variable_name} set to {value}.")
        except Exception as e:
            print(f"Error setting value: {e}")

    def do_list_features(self, arg):
        """List all available features of the selected sensor."""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        features = list(self.selected_sensor.features.keys())
        if features:
            print("Available features:")
            for f in features:
                print(f"- {f}")
        else:
            print("No features available.")

    def do_list_stfts(self, arg):
        """List all available STFTs of the selected sensor."""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        if self.selected_sensor.stfts:
            print("Available STFTs:")
            for stft in self.selected_sensor.stfts:
                print(f"- {stft.id}")
        else:
            print("No STFTs available.")

    def do_add_stft(self, arg):
        """Add a new STFT to the selected sensor.
Syntax: add_stft <stft_id> <window_size> <window_type> <hop_size>
Example: add_stft stft_1 512 hann 256

A newly added STFT is automatically assigned the provided ID and computed using the RAW feature if available.
        """
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return

        parts = arg.split()
        if len(parts) != 4:
            print("Usage: add_stft <stft_id> <window_size> <window_type> <hop_size>")
            return

        stft_id = parts[0]
        try:
            window_size = int(parts[1])
            window_type = parts[2]
            hop_size = int(parts[3])
        except Exception as e:
            print("Invalid parameter format:", e)
            return

        # Hier wird davon ausgegangen, dass die Sensor-Klasse eine add_stft-Methode besitzt,
        # die nun auch einen Parameter 'stft_id' entgegennimmt.
        self.selected_sensor.add_stft(stft_id=stft_id, window_size=window_size, window_type=window_type, hop_size=hop_size)
        # Hole den neu hinzugefügten STFT (angenommen, er ist das letzte Element in der Liste)
        new_stft = self.selected_sensor.stfts[-1]
        # Automatische Berechnung, falls das RAW-Feature existiert
        raw_feature = self.selected_sensor.get_feature("Raw")
        if raw_feature is not None:
            new_stft.compute_stft(raw=raw_feature)
            print(f"STFT {new_stft.id} added and computed with window_size={window_size}, window_type='{window_type}', hop_size={hop_size}.")
        else:
            print(f"STFT {new_stft.id} added, but RAW feature not found. STFT not computed.")

    def do_remove_stft(self, arg):
        """Remove an STFT from the selected sensor.
Syntax: remove_stft <stft_id>
Example: remove_stft stft_1
        """
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        if not arg:
            print("Usage: remove_stft <stft_id>")
            return
        try:
            self.selected_sensor.remove_stft(stft_id=arg)
            print(f"STFT with ID {arg} removed.")
        except Exception as e:
            print(f"Error removing STFT: {e}")

    def do_set_type(self, arg):
        """Remove an STFT from the selected sensor.
Syntax: remove_stft <stft_id>
Example: remove_stft stft_1
        """
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        if not arg or (arg != "MICROPHONE" and arg != "ACCELERATOR"):
            print("Usage: set_type <MICROPHONE/ACCELERATOR>")
            return
        try:
            self.selected_sensor.sensortype = arg

        except Exception as e:
            print(f"Error removing STFT: {e}")

    def do_revaluate_all(self, arg):
        """Reevaluate all STFTs for the selected sensor.
If the RAW feature is available, its values are used for reevaluation.
Syntax: revaluate_all
        """
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return

        raw_feature = self.selected_sensor.get_feature("Raw")
        if raw_feature is None:
            print("No RAW feature found in the selected sensor. Revaluating without new raw data.")
        for stft in self.selected_sensor.stfts:
            try:
                stft.re_evaluate(raw=raw_feature.values if raw_feature is not None else None)
                print(f"STFT {stft.id} re-evaluated.")
            except Exception as e:
                print(f"Error re-evaluating STFT {stft.id}: {e}")

    def do_revaluate_stft(self, arg):
        """Reevaluate a specific STFT.
Syntax: revaluate_stft <stft_id>
If the RAW feature is available, its values are used for reevaluation.
        """
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        if not arg:
            print("Usage: revaluate_stft <stft_id>")
            return
        # Suche den STFT mit der angegebenen ID
        target_stft = None
        for stft in self.selected_sensor.stfts:
            if stft.id == arg:
                target_stft = stft
                break
        if target_stft is None:
            print(f"No STFT with ID {arg} found.")
            return
        raw_feature = self.selected_sensor.get_feature("Raw")
        try:
            target_stft.re_evaluate(raw=raw_feature.values if raw_feature is not None else None)
            print(f"STFT {arg} re-evaluated.")
        except Exception as e:
            print(f"Error re-evaluating STFT {arg}: {e}")

    def do_print_sensor(self, arg):
        """Print details of the selected sensor."""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        sensor = self.selected_sensor
        print("Sensor Details:")
        print(f"  ID: {sensor.sensorid}")
        print(f"  Alias: {sensor.alias}")
        print(f"  Type: {sensor.sensortype}")
        print(f"  Measure Time: {sensor.measure_time}")
        print(f"  Location: {sensor.location}")
        print(f"  Description: {sensor.description}")
        print("\nFeatures:")
        if sensor.features:
            for key, feature in sensor.features.items():
                print(f"  - {key}: {feature}")
        else:
            print("  None")
        print("\nSTFTs:")
        if sensor.stfts:
            for stft in sensor.stfts:
                print(f"  - {stft.id}: window_size={stft.window_size}, hop_size={stft.hop_size}, window_function={stft.window_function}")
        else:
            print("  None")

    def do_update_sensor(self, arg):
        """Dummy command to simulate sensor update."""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return
        # Hier könnte Logik zur Aktualisierung des Sensors ergänzt werden.
        print(f"Sensor {self.selected_sensor.sensorid} updated.")

if __name__ == "__main__":
    SensorConsole().cmdloop()
