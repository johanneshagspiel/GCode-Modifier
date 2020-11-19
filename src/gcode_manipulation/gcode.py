
class GCode:

    def __init__(self):
        self.start_gcode = []
        self.main_gcode = []
        self.end_gcode = []

        self.layer_index_list = []
        self.time_elapsed_index_list = []
        self.movements_per_layer_list = []

        self.amount_layers = 0
        self.largest_extrusion_value = 0
