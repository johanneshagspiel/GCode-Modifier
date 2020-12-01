from paste_printer.gcode_manipulation.gcode import GCode

class Gcode_Writer():

    def __init__(self):
        self.start_gcode = None
        self.end_gcode = None

    def set_flowrate_layer_0(self, flowrate_layer_0):
        text = "M221 S" + str(flowrate_layer_0) + "; Set Flowrate Layer 0"

        new_main_body = []

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            if ";LAYER:0" in line:
                new_main_body.append(text)

        self.end_gcode.main_body = new_main_body
        return self.end_gcode

    def set_flowrate_other_layers(self, flowrate_other_layers):
        text = "M221 S" + str(flowrate_other_layers) + "; Set Flowrate Other Layers"

        new_main_body = []

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            if ";LAYER:1" in line:
                new_main_body.append(text)

        self.end_gcode.main_body = new_main_body
        return self.end_gcode

    def set_bed_temperature(self, bed_temperature):
        text = "M140 S" + str(bed_temperature) + "; Set Bed Temperature"

        new_main_body = []
        new_main_body.append(text)

        for line in self.start_gcode.main_body:
            new_main_body.append(line)

        self.end_gcode.main_body = new_main_body

        return self.end_gcode

    def additional_information(self):

        new_start = []
        new_start.append("M117 Print is starting; Additional Information")
        for line in self.end_gcode.startup_code:
            new_start.append(line)
        self.end_gcode.startup_code = new_start

        new_main = []
        current_layer = 0
        current_move = 1

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        for index, line in enumerate(self.end_gcode.main_body):
            if any(x in line for x in movement_commands):
                if current_move % 3 == 0 or current_move == self.end_gcode.movements_per_layer_list[current_layer] or current_move == 1:
                    text = "M117 Mov " + str(current_move) + "/" + str(self.end_gcode.movements_per_layer_list[current_layer]) \
                           + " Lay " + str(current_layer + 1) + "/" + str(self.end_gcode.amount_layers) + "; Additional Information"
                    new_main.append(text)

                current_move += 1

            new_main.append(line)

            if index == self.end_gcode.time_elapsed_index_list[current_layer]:
                current_layer += 1
                current_move = 1

        self.end_gcode.main_body = new_main

        new_end = []
        new_end.append("M117 Print is winding down; Additional Information")
        for line in self.end_gcode.shutdown_code:
            new_end.append(line)
        self.end_gcode.shutdown_code = new_end

        return self.end_gcode

    def pause_each_layer(self, pause_in_seconds):

        previous_index = 0
        last_index = len(self.start_gcode.main_body)

        gcode_list = []
        print(str(pause_in_seconds))
        for layer_index in self.start_gcode.time_elapsed_index_list:

            for index in range(previous_index, layer_index):
                gcode_list.append(self.start_gcode.main_body[index])

            gcode_list.append("G1 E-40 ; Stop each Layer - Retract a bit")
            gcode_list.append("G4 S" + str(pause_in_seconds) + "; Stop each Layer - Wait")
            gcode_list.append("G1 E40 ; Re-extrude a bit")

            previous_index = layer_index

        for index in range(previous_index, last_index):
            gcode_list.append(self.start_gcode.main_body[index])

        self.end_gcode.main_body = gcode_list

        return self.end_gcode

    def retract_syringe(self):

        if self.start_gcode.largest_extrusion_value <= 1000:
            largest_one_time_retraction = self.start_gcode.largest_extrusion_value
            still_to_rectract = 0
            repeat_insertion = False
        else:
            largest_one_time_retraction = 1000
            still_to_rectract = self.start_gcode.largest_extrusion_value - 1000
            repeat_insertion = True

        new_end_gcode = []

        for index, line in enumerate(self.start_gcode.shutdown_code):
            new_end_gcode.append(line)
            if "G1 X0 Y220" in line:
                while repeat_insertion is True:
                    new_reverse_extrusion = "G1 E-" + str(largest_one_time_retraction) + "; retract syringe"
                    new_end_gcode.append(new_reverse_extrusion)

                    if still_to_rectract > 0:
                        if still_to_rectract <= 1000:
                            largest_one_time_retraction = still_to_rectract
                            still_to_rectract = 0
                        else:
                            temp = still_to_rectract
                            largest_one_time_retraction = still_to_rectract - 1000
                            still_to_rectract = temp - largest_one_time_retraction
                    else:
                        repeat_insertion = False

        self.end_gcode.shutdown_code = new_end_gcode

        return self.end_gcode

    def set_gcode(self, new_gcode: GCode):
        self.start_gcode = new_gcode
        self.end_gcode = new_gcode