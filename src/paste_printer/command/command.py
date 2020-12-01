
class Command():

    def __init__(self, path_to_file, flow_rate_layer_0, flow_rate_other_layers, bed_temperature, additional_information_bol, pause_each_layer_bol, retract_syringe_bol, file_name, storage_path, pause_each_layer_par = None):
        self.path_to_file = path_to_file

        self.flow_rate_layer_0 = flow_rate_layer_0
        self.flow_rate_other_layers = flow_rate_other_layers
        self.bed_temperature = bed_temperature

        self.additional_information_bol = additional_information_bol
        self.pause_each_layer_bol = pause_each_layer_bol
        self.retract_syringe_bol = retract_syringe_bol

        self.file_name = file_name
        self.storage_path = storage_path

        self.pause_each_layer_par = pause_each_layer_par
