
class Command():

    def __init__(self, flow_rate, bed_temperature, add_information, stop_each_layer, retract_syringe_end_of_print, file_name, storage_path):
        self.flow_rate = flow_rate
        self.bed_temperature = bed_temperature

        self.add_information = add_information
        self.stop_each_layer = stop_each_layer
        self.retract_syringe_end_of_print = retract_syringe_end_of_print

        self.file_name = file_name
        self.storage_path = storage_path

