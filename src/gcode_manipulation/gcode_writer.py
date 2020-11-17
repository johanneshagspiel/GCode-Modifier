from gcode_manipulation.gcode import GCode
from gcode_manipulation.gcode_parser import GCode_Parser

class Gcode_Writer():

    def __init__(self,gcode: GCode):
        self.original_gcode = gcode
        self.modified_gcode = GCode()
        self.parser = GCode_Parser(gcode=self.modified_gcode)

    def modify_gcode(self):

        self.add_pause_end_each_layer()

        return self.modified_gcode

    def update_information(self):
        self.parser.find_indexes()

    def add_pause_end_each_layer(self):

        previous_index = 0
        last_index = len(self.original_gcode.main_gcode)

        gcode_list = []

        for layer_index in self.original_gcode.time_elapsed_list:

            for index in range(previous_index, layer_index):
                gcode_list.append(self.original_gcode.main_gcode[index])

            gcode_list.append("G4 S10")
            previous_index = layer_index

        for index in range(previous_index, last_index):
            gcode_list.append(self.original_gcode.main_gcode[index])

        self.modified_gcode.main_gcode = gcode_list

        self.update_information()

