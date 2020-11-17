from pathlib import Path
from gcode_parser.gcode import GCode

class GCode_Parser:

    def __init__(self):
        self.root = Path(__file__).parents[2]
        self.gcode = GCode()

    def create_gcode(self):
        self.read_file()
        self.analyze_gcode()

        return self.gcode

    def read_file(self):
        file_path = Path.joinpath(self.root, "resources", "CFFFP_20mm_Calibration_Box (half cube).gcode")

        line_list = []
        with open(file_path, 'r') as f:
            line_list = [line.strip() for line in f if line.strip()]

        self.gcode.original_gcode = line_list

    def analyze_gcode(self):

        index_list = []
        for index, line in enumerate(self.gcode.original_gcode):
            if ";LAYER:" in line:
                index_list.append(index)

        self.gcode.layer_index = index_list