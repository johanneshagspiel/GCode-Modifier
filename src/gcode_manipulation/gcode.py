
class GCode:

    def __init__(self):
        self.startup_code = []
        self.main_body = []
        self.shutdown_code = []

        self.layer_index_list = []
        self.time_elapsed_index_list = []
        self.movements_per_layer_list = []

        self.amount_layers = 0
        self.largest_extrusion_value = 0
