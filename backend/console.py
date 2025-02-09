import cmd
import os
from backend.data.DeviceData import DeviceData
from backend.utils.SensorType import Sensortype

class SensorConsole(cmd.Cmd):
    prompt = ">>> "  # User prompt
    intro = "Welcome to the Sensor Data Console! Choose an option: (1) Load File (2) Convert File (3) Exit"

    def __init__(self):
        super().__init__()
        self.device = None
        self.selected_sensor = None

    def do_load(self, arg):
        """Load sensor data from a YAML file. Syntax: 1 <directory_path>"""
        if not arg:
            print("Please specify a directory.")
            return

        if not os.path.exists(arg):
            print(f"Directory {arg} does not exist!")
            return

        self.device = DeviceData(dir=arg)
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
        """Executes DeviceData.introduce() method."""
        if not self.device:
            print("No device loaded. Use '1 <directory>' first.")
            return
        self.device.introduce()

    def do_save(self, arg):
        """Save all sensor data to a directory. Syntax: save <directory>"""
        if not self.device:
            print("No device loaded. Use '1 <directory>' first.")
            return

        if not arg:
            print("Please specify a directory.")
            return

        self.device.save(arg)
        print(f"Data saved to {arg}.")

    def do_select(self, arg):
        """Select a sensor by ID. Syntax: select <sensor_id>"""
        if not self.device:
            print("No device loaded. Use '1 <directory>' first.")
            return

        for sensor in self.device.sensors:
            if sensor.sensorID == arg:
                self.selected_sensor = sensor
                print(f"Sensor {arg} selected. Use 'getVariable <variable>' or 'getPath'.")
                return
        print(f"Sensor {arg} not found.")

    def do_getValue(self, arg):
        """Retrieve a variable from the selected sensor. Syntax: getVariable <variable_name>"""
        if not self.selected_sensor:
            print("No sensor selected. Use 'select <sensor_id>' first.")
            return

        if hasattr(self.selected_sensor, arg):
            print(f"{arg}: {getattr(self.selected_sensor, arg)}")
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
        if hasattr(self.selected_sensor, variable_name):
            try:
                setattr(self.selected_sensor, variable_name, eval(value))
                print(f"{variable_name} set to {value}.")
            except Exception as e:
                print(f"Error setting value: {e}")
        else:
            print(f"Variable '{variable_name}' does not exist in the selected sensor.")


if __name__ == "__main__":
    SensorConsole().cmdloop()