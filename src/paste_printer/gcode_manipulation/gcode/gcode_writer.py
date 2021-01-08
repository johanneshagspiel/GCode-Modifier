from paste_printer.gcode_manipulation.gcode.gcode import GCode

class Gcode_Writer():

    def __init__(self, settings):
        self.start_gcode = None
        self.end_gcode = None

        self.settings = settings

    def set_flowrate_layer_0(self, flowrate_layer_0):
        text = "M221 S" + str(flowrate_layer_0) + " ; Set Flowrate Layer 0"

        new_main_body = []

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            if ";LAYER:0" in line:
                new_main_body.append(text)

        self.end_gcode.main_body = new_main_body
        return self.end_gcode

    def set_flow_rate_other_layers(self, flow_rate):
        new_main_body = []

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            if line == ";LAYER:1":
                text = "M221 S" + str(flow_rate) + " ; Set Flowrate Other Layers"
                new_main_body.append(text)

        self.end_gcode.main_body = new_main_body
        return self.end_gcode

    def set_flow_rate_outer_walls_infill(self, flow_rate_outer_walls, flow_rate_infill):
        new_main_body = []

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            if ";TYPE:WALL-OUTER" in line:
                text = "M221 S" + str(flow_rate_outer_walls) + " ; Set Flowrate Outer Walls"
                new_main_body.append(text)
            if ";TYPE:SKIN" in line:
                text = "M221 S" + str(flow_rate_infill) + " ; Set Flowrate Infill"
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

    def set_print_speed(self, print_speed):

        speed_multiplier= float(print_speed) / 100;
        new_main = []
        movement_commands = ["G0", "G1", "G2", "G3", "G5"]

        for index, line in enumerate(self.start_gcode.main_body):
            split_line = line.split()
            if split_line[0] in movement_commands:
                for index, word in enumerate(split_line):
                    if "F" in word:
                        current_speed = float(word[1:])
                        new_speed = current_speed * speed_multiplier
                        split_line[index] = "F" + str(new_speed)
                line = " ".join(split_line)
            new_main.append(line)

        self.end_gcode.main_body = new_main
        return self.end_gcode

    def turn_on_fan(self):

        turn_on_fan_text = "M106 ; Turn On The Fan"
        new_main_body = []
        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        first_time = True

        for line in self.start_gcode.main_body:
            new_main_body.append(line)
            split_line = line.split()
            if split_line[0] in movement_commands and first_time:
                new_main_body.append(turn_on_fan_text)
                first_time = False

        turn_off_fan_text = "M107 ; Turn Off The Fan"
        new_shutdown_code = []

        new_shutdown_code.append(turn_off_fan_text)

        for line in self.start_gcode.shutdown_code:
            new_shutdown_code.append(line)

        self.end_gcode.main_body = new_main_body
        self.end_gcode.shutdown_code = new_shutdown_code

        return self.end_gcode

    def additional_information(self):

        new_start = []
        new_start.append("M117 Print is starting; Additional Information")
        for line in self.start_gcode.startup_code:
            new_start.append(line)

        new_main = []
        current_layer = 0
        current_move = 1

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        for index, line in enumerate(self.start_gcode.main_body):
            new_main.append(line)
            split_line = line.split()
            if split_line[0] in movement_commands:
                if current_move % 5 == 0 or current_move == self.start_gcode.movements_per_layer_list[current_layer] or current_move == 1:
                    text = "M117 Mov " + str(current_move) + "/" + str(self.start_gcode.movements_per_layer_list[current_layer]) \
                           + " Lay " + str(current_layer + 1) + "/" + str(self.start_gcode.amount_layers) + "; Additional Information"
                    new_main.append(text)

                current_move += 1

            if index == self.start_gcode.time_elapsed_index_list[current_layer]:
                current_layer += 1
                current_move = 1

        new_end = []
        new_end.append("M117 Print is winding down; Additional Information")
        for line in self.start_gcode.shutdown_code:
            new_end.append(line)

        self.end_gcode.startup_code = new_start
        self.end_gcode.main_body = new_main
        self.end_gcode.shutdown_code = new_end

        return self.end_gcode

    def pause_each_layer(self, pause_in_seconds, retract_bol):

        previous_index = 0
        last_index = len(self.start_gcode.main_body)

        gcode_list = []
        for layer_index in self.start_gcode.time_elapsed_index_list:

            for index in range(previous_index, layer_index):
                gcode_list.append(self.start_gcode.main_body[index])

            gcode_list.append("G60 S0 ; Save Current Position To Return To")
            if retract_bol == True:
                gcode_list.append("G1 E-1 ; Stop each Layer - Retract a bit")
            gcode_list.append("G28 X ; Auto Home To Move Out Of Way")
            gcode_list.append("G4 S" + str(pause_in_seconds) + " ; Stop each Layer - Wait")
            gcode_list.append("M117 Pause "+ str(pause_in_seconds) + " seconds")
            if retract_bol == True:
                gcode_list.append("G1 E1 ; Re-extrude a bit")
            gcode_list.append("G61 XYZ S0; Return To The Saved Position")

            previous_index = layer_index

        for index in range(previous_index, last_index):
            gcode_list.append(self.start_gcode.main_body[index])

        self.end_gcode.main_body = gcode_list

        return self.end_gcode

    def clean_nozzle(self, amount_of_moves):

        amount_of_moves_int = int(amount_of_moves)

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]

        new_main=[]
        current_speed = 0
        current_x_position = 0
        current_y_position = 0
        current_z_position = 0
        current_movements_seen = 0

        for line in self.start_gcode.main_body:
            new_main.append(line)
            split_line = line.split()
            #In the gcode format the movement command should be the first word
            if split_line[0] in movement_commands:
                current_movements_seen += 1
                for word in split_line:
                    if "F" in word:
                        current_speed = float(word[1:])
                    if "X" in word:
                        current_x_position = float(word[1:])
                    if "Y" in word:
                        current_y_position = float(word[1:])
                    if "Z" in word:
                        current_z_position = float(word[1:])
            if current_movements_seen != 0 and current_movements_seen % amount_of_moves_int == 0:
                x_border_sponge = self.settings.environment.printer.bed_width_x - self.settings.environment.sponge.width_x - 2 # 2 is a small offsett - we do not want to hit the sponge
                y_border_sponge = self.settings.environment.sponge.depth_y + 2
                z_border_sponge = self.settings.environment.sponge.height_z + 2

                new_main.append("G0 F600 X" + str(x_border_sponge) + " Y" + str(y_border_sponge) + " ; Move To The Top Left Border Of The Sponge")
                new_main.append("G0 Z" + str(z_border_sponge) + " ; Move Slightly Above The Height Of The Sponge")

                x_mid_sponge = self.settings.environment.printer.bed_width_x - (self.settings.environment.sponge.width_x / 2)
                y_mid_sponge = self.settings.environment.sponge.depth_y / 2

                new_main.append("G0 X" + str(x_mid_sponge) + " Y" + str(y_mid_sponge) + " ; Move To The Middle Of The Sponge")

                # Set How often it goes up and down
                for iteration in range(6):
                    new_main.append("G0 Z0 ; Move Down")
                    new_main.append("G0 Z" + str(z_border_sponge) + " ; Move Up")

                new_main.append("G0 F600 X" + str(x_border_sponge) + " Y" + str(y_border_sponge) + " ; Move Back To The Top Left Border Of The Sponge")
                new_main.append("G0 X" + str(current_x_position) +" Y" + str(current_y_position) + " Z" + str(current_z_position) + " ; Move to Back To Previous Print Position")
                new_main.append("G0 F" + str(current_speed) + " ; Set Speed Back")
                current_movements_seen = 0

        self.end_gcode.main_body = new_main

        return self.end_gcode

    def retract_syringe(self):

        max_one_time_extrusion = 1000

        if self.start_gcode.largest_extrusion_value <= max_one_time_extrusion:
            largest_one_time_retraction = self.start_gcode.largest_extrusion_value
            still_to_rectract = 0
        else:
            largest_one_time_retraction = max_one_time_extrusion
            still_to_rectract = self.start_gcode.largest_extrusion_value - max_one_time_extrusion
        repeat_insertion = True

        new_end_gcode = []

        for index, line in enumerate(self.start_gcode.shutdown_code):
            new_end_gcode.append(line)
            if "G1 X0 Y220" in line:
                new_end_gcode.append("M83 ; Set eXtrusion Mode To Relative During Retraction")
                while repeat_insertion is True:
                    new_reverse_extrusion = "G0 E-" + str(largest_one_time_retraction) + " ; Retract Syringe"
                    new_end_gcode.append(new_reverse_extrusion)

                    if still_to_rectract > 0:
                        if still_to_rectract <= max_one_time_extrusion:
                            largest_one_time_retraction = still_to_rectract
                            still_to_rectract = 0
                        else:
                            temp = still_to_rectract
                            still_to_rectract = temp - max_one_time_extrusion
                            largest_one_time_retraction = max_one_time_extrusion
                    else:
                        repeat_insertion = False
                new_end_gcode.append("M82 ; Set eXtrusion Mode Back To Absolute")

        self.end_gcode.shutdown_code = new_end_gcode

        return self.end_gcode

    def set_gcode(self, new_gcode: GCode):
        self.start_gcode = new_gcode
        self.end_gcode = new_gcode
        