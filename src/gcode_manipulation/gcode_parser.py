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

        new_gcode.main_gcode = self.file_handler.read_file()
        self.gcode = new_gcode

    def analyze_gcode(self):
        self.split_gcode()
        self.find_indexes()

    def split_gcode(self):

        start_gcode = []
        main_gcode = []
        main_gcode_to_be_flatten = []
        end_gcode = []

        before_layer_0 = True
        temp_list = []

        for line in self.gcode.main_gcode:
            if ";LAYER:0" in line:
                before_layer_0 = False
            if before_layer_0 is True:
                start_gcode.append(line)
            elif ";TIME_ELAPSED:" in line:
                temp_list.append(line)
                main_gcode_to_be_flatten.append(temp_list)
                temp_list = []
            else:
                temp_list.append(line)

        end_gcode = temp_list

        for sublist in main_gcode_to_be_flatten:
            for item in sublist:
                main_gcode.append(item)

        self.gcode.start_gcode = start_gcode
        self.gcode.main_gcode = main_gcode
        self.gcode.end_gcode = end_gcode

    def find_indexes(self):

        layer_list = []
        time_elapsed_list =[]
        movements_per_layer_list = []

        current_layer = -1

        for index, line in enumerate(self.gcode.main_gcode):
            if ";LAYER:" in line:
                layer_list.append(index)
                current_layer += 1
                movements_per_layer_list.append(0)
            if "G0" or "G1" or "G2" or "G3" or "G5" in line:
                movements_per_layer_list[current_layer] += 1
            if ";TIME_ELAPSED:" in line:
                time_elapsed_list.append(index)

        self.gcode.layer_index_list = layer_list
        self.gcode.amount_layers = len(layer_list)
        self.gcode.time_elapsed_index_list = time_elapsed_list
        self.gcode.movements_per_layer_list = movements_per_layer_list