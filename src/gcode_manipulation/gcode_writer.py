from gcode_manipulation.gcode import GCode
from gcode_manipulation.gcode_parser import GCode_Parser

class Gcode_Writer():

    def __init__(self,gcode: GCode):
        self.original_gcode = gcode
        self.modified_gcode = gcode
        self.parser = GCode_Parser(gcode=self.modified_gcode)

    def modify_gcode(self):

        #self.add_pause_end_each_layer()
        self.add_information_text()

        return self.modified_gcode

    def update_information(self):
        self.parser.find_indexes()

    def add_pause_end_each_layer(self):

        previous_index = 0
        last_index = len(self.original_gcode.main_gcode)

        gcode_list = []

        for layer_index in self.original_gcode.time_elapsed_index_list:

            for index in range(previous_index, layer_index):
                gcode_list.append(self.original_gcode.main_gcode[index])

            gcode_list.append("G4 S10")
            previous_index = layer_index

        for index in range(previous_index, last_index):
            gcode_list.append(self.original_gcode.main_gcode[index])

        self.modified_gcode.main_gcode = gcode_list

        self.update_information()

    def add_information_text(self):

        new_start = []
        new_start.append("M117 Print is starting")
        for line in self.modified_gcode.start_gcode:
            new_start.append(line)
        self.modified_gcode.start_gcode = new_start

        new_main = []
        current_layer = 0
        current_move = 0

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]

        for index, line in enumerate(self.modified_gcode.main_gcode):
            if any(x in line for x in movement_commands):
                text = "M117 Mov " + str(current_move) + "/" + str(self.modified_gcode.movements_per_layer_list[current_layer]) + " Lay " + str(current_layer + 1) + "/" + str(self.modified_gcode.amount_layers)
                new_main.append(text)
                current_move += 1
            new_main.append(line)

            if index == self.modified_gcode.time_elapsed_index_list[current_layer]:
                current_layer += 1
                current_move = 0

        self.modified_gcode.main_gcode = new_main

        new_end = []
        new_end.append("M117 Print is winding down")
        for line in self.modified_gcode.end_gcode:
            new_end.append(line)
        self.modified_gcode.end_gcode = new_end

        self.update_information()
