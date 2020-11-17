from gcode_manipulation.gcode import GCode
from util.file_handler import File_Handler

class GCode_Parser:

    def __init__(self,gcode: GCode = None):
        self.gcode = gcode
        self.file_handler = File_Handler()

    def create_gcode(self):
        self.setup_gcode()
        self.analyze_gcode()

        return self.gcode

    def setup_gcode(self):
        new_gcode = GCode()

        new_gcode.gcode_list = self.file_handler.read_file()
        self.gcode = new_gcode

    def analyze_gcode(self):
        self.find_indexes()

    def find_indexes(self):

        layer_list = []
        time_elapsed_list =[]

        for index, line in enumerate(self.gcode.gcode_list):
            if ";TIME_ELAPSED:" in line:
                time_elapsed_list.append(index)
            if ";LAYER:" in line:
                layer_list.append(index)

        self.gcode.layer_list = layer_list
        self.gcode.time_elapsed_list = time_elapsed_list