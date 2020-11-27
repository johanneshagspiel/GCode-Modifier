from enum import Enum

class Task (Enum):
    SET_FLOWRATE = 1
    SET_BED_TEMPERATURE = 2

    ADDITIONAL_INFORMATION = 3
    PAUSE_EACH_LAYER = 4
    RETRACT_SYRINGE = 5
