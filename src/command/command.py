
class Command():

    def __init__(self, path_to_file, flow_rate, bed_temperature, additional_information, pause_each_layer, retract_syringe, file_name, storage_path):
        self.path_to_file = path_to_file

        self.flow_rate = flow_rate
        self.bed_temperature = bed_temperature

        self.additional_information = additional_information
        self.pause_each_layer = pause_each_layer
        self.retract_syringe = retract_syringe

        self.file_name = file_name
        self.storage_path = storage_path
