from enum import Enum
from typing import Callable



class Sensortype(Enum):
    MICROPHONE = (1, "microphone")
    ACCELERATOR = (2, "accelerator")
    VOLTMETER = (3, "voltmeter")

    def __new__(cls, id: int, name: str):
        obj = object.__new__(cls)
        obj._value_ = id
        obj._name_ = name
        return obj;




    def get_sensortype_by_id(id : int):
        for type in Sensortype:
            if(type._value_ == id):
                return type;
        return None

    def get_sensortype_by_name(name : str):

        for type in Sensortype:
            if(type.name == name):
                return type;
        return None