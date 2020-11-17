from gcode_manipulation.gcode import GCode
from gcode_manipulation.gcode_parser import GCode_Parser

class Gcode_Writer():

    def __init__(self,gcode: GCode):
        self.original_gcode = gcode
        self.modified_gcode = GCode()
        self.parser = GCode_Parser()

    def modify_gcode(self):

        self.add_pause_end_each_layer()

        return self.modified_gcode

    def add_pause_end_each_layer(self):

        previous_index = 0
        last_index = len(self.original_gcode.gcode_list)

        gcode_list = []

        for layer_index in self.original_gcode.layer_index_list:

            for index in range(previous_index, layer_index-1):
                gcode_list.append(self.original_gcode.gcode_list[index])

            gcode_list.append("M25")
            previous_index = layer_index

        for index in range(previous_index, last_index):
            gcode_list.append(self.original_gcode.gcode_list[index])

        self.modified_gcode.gcode_list = gcode_list

        self.parser.find_layer_index(self.modified_gcode)