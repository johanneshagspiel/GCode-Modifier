from paste_printer.gcode_manipulation.gcode.gcode import GCode
from paste_printer.gcode_manipulation.layer.layer_parser import Layer_Parser

class GCode_Parser:

    def __init__(self, line_list):
        self.line_list = line_list

        self.layer_parser = Layer_Parser()

        self.start_gcode = None
        self.end_gcode = None

    def create_gcode(self):
        new_gcode = GCode()
        new_gcode.whole_code = self.line_list
        self.set_gcode(new_gcode)

        analyzed_result = self.analyze_gcode()

        return analyzed_result

    def analyze_gcode(self):
        split_result = self.split_gcode()
        self.set_gcode(split_result)

        cleaned_result = self.clean_gcode()
        self.set_gcode(cleaned_result)

        self.end_gcode = self.find_indexes()

        return self.end_gcode

    def split_gcode(self):

        startup_code = []
        main_body_to_be_flatten = []
        main_body = []

        layer_list_to_be_parsed = []
        layer_list = []

        shutdown_code = []

        before_layer_0 = True
        current_layer = []

        for line in self.start_gcode.whole_code:
            if ";LAYER:0" in line:
                before_layer_0 = False
            if before_layer_0 is True:
                startup_code.append(line)
            elif ";TIME_ELAPSED:" in line:
                current_layer.append(line)
                main_body_to_be_flatten.append(current_layer)
                layer_list_to_be_parsed.append(current_layer)
                current_layer = []
            else:
                current_layer.append(line)

        shutdown_code = current_layer

        for sublist in main_body_to_be_flatten:
            for item in sublist:
                main_body.append(item)

        layer_list = self.layer_parser.parse_layer_list(layer_list_to_be_parsed)

        self.end_gcode.startup_code = startup_code
        self.end_gcode.main_body = main_body
        self.end_gcode.layer_list = layer_list
        self.end_gcode.shutdown_code = shutdown_code

        return self.end_gcode

    def clean_gcode(self):

        start_cura_bol = True
        start_cura_list = []
        layer_count_list = []

        for line in self.start_gcode.startup_code:
            if start_cura_bol is True:
                start_cura_list.append(line)
                if ";Generated with" in line:
                    start_cura_bol = False
            if ";LAYER_COUNT" in line:
                layer_count_list.append(line)

        new_start_cura_list = []
        new_start_cura_list.append("M105")
        new_start_cura_list.append("M109 S0")
        new_start_cura_list.append("M82 ;absolute extrusion mode")
        new_start_cura_list.append("M302 P1")
        new_start_cura_list.append("M106 S0")
        new_start_cura_list.append("G92 E0")
        new_start_cura_list.append("G28 ; Manual Bedleveling (?)")
        new_start_cura_list.append("G1 Z5.0 F3000")
        new_start_cura_list.append("G92 E0")
        new_start_cura_list.append("G92 E0")

        new_start = start_cura_list + layer_count_list + new_start_cura_list
        self.end_gcode.startup_code = new_start


        new_main = []
        for line in self.start_gcode.main_body:
            if "M140" not in line:
                new_main.append(line)

        self.end_gcode.main_body = new_main

        new_end = []
        new_end.append("M140 S0")
        new_end.append("G91")
        new_end.append("G1 Z1.1 F2400")
        new_end.append("G1 X5 Y5 F3000")
        new_end.append("G1 Z10")
        new_end.append("G90")
        new_end.append("G1 X0 Y220")
        new_end.append("M106 S0")
        new_end.append("M104 S0")
        new_end.append("M140 S0")
        new_end.append("M84 E X Y E")
        new_end.append("M302 P0")
        new_end.append("M82 ;absolute extrusion mode")

        for line in self.start_gcode.shutdown_code:
            if ";SETTING_3" in line:
                new_end.append(line)

        self.end_gcode.shutdown_code = new_end

        return self.end_gcode


    def find_indexes(self):

        layer_list = []
        time_elapsed_list =[]
        movements_per_layer_list = []

        current_layer = -1
        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        largest_extrusion_value = 0

        for index, line in enumerate(self.start_gcode.main_body):
            if ";LAYER:" in line:
                layer_list.append(index)
                current_layer += 1
                movements_per_layer_list.append(0)
            elif any(x in line for x in movement_commands):
                movements_per_layer_list[current_layer] += 1

                split_line = line.split()
                for word in split_line:
                    if "E" in word:
                        extrusion_value = float(word[1:])
                        if extrusion_value > largest_extrusion_value:
                            largest_extrusion_value = extrusion_value

            elif ";TIME_ELAPSED:" in line:
                time_elapsed_list.append(index)

        self.end_gcode.layer_index_list = layer_list
        self.end_gcode.time_elapsed_index_list = time_elapsed_list
        self.end_gcode.movements_per_layer_list = movements_per_layer_list

        self.end_gcode.amount_layers = len(layer_list)
        self.end_gcode.largest_extrusion_value = largest_extrusion_value

        return self.end_gcode

    def improve_gcode_at_the_end(self):

        return self.end_gcode

    def create_final_gcode(self):

        startup_string = "\n".join(self.end_gcode.startup_code)
        startup_string += "\n\n\n"
        main_body_string = "\n".join(self.end_gcode.main_body)
        main_body_string += "\n\n\n"
        shutdown_string = "\n".join(self.end_gcode.shutdown_code)

        self.end_gcode.whole_code = startup_string + main_body_string + shutdown_string

        return self.end_gcode

    def set_gcode(self, new_gcode: GCode):
        self.start_gcode = new_gcode
        self.end_gcode = new_gcode
