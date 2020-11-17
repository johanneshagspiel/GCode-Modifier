from pathlib import Path
from gcode_manipulation.gcode import GCode

class GCode_Parser:

    def __init__(self):
        self.root = Path(__file__).parents[2]

    def create_gcode(self):
        created_gcode = self.read_file()
        result = self.analyze_gcode(created_gcode)

        return result

    def read_file(self):
        new_gcode = GCode()

        file_path = Path.joinpath(self.root, "resources", "CFFFP_20mm_Calibration_Box (half cube).gcode")
        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        new_gcode.gcode_list = line_list
        return new_gcode

    def analyze_gcode(self, gcode):
        gcode = self.find_layer_index(gcode)
        return gcode

    def find_layer_index(self, gcode):

        index_list = []
        for index, line in enumerate(gcode.gcode_list):
            if ";LAYER:" in line:
                index_list.append(index)

        gcode.layer_index_list = index_list

        return gcode