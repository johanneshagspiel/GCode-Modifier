from paste_printer.gcode_manipulation.gcode.layer import Layer


class Layer_Parser():

    def __init__(self):
        None

    def parse_layer(self, string_to_be_parsed):
        layer = Layer()

        layer.layer_as_string = string_to_be_parsed

        movement_commands = ["G0", "G1", "G2", "G3", "G5"]
        largest_extrusion_value = 0

        for index, line in enumerate(string_to_be_parsed):
            if ";" in line[0]:
                if "LAYER:" in line:
                    layer_number = line.split(":")[1]
                    layer.number = int(layer_number)
            else:
                if any(x in line for x in movement_commands):
                    split_line = line.split()
                    for word in split_line:
                        if "E" in word:
                            extrusion_value = float(word[1:])
                            if extrusion_value > largest_extrusion_value:
                                largest_extrusion_value = extrusion_value
                        if "X" in word:
                            x_position = float(word[1:])
                            layer.x_data.append(x_position)
                        if "Y" in word:
                            y_position = float(word[1:])
                            layer.y_data.append(y_position)

        layer.largest_extrusion_value = largest_extrusion_value

        return layer
