
class Command():

    def __init__(self, path_to_file,
                 flow_rate_layer_0, flow_rate_par_1, flow_rate_differentiate_bol,
                 bed_temperature, print_speed, fan_bol,
                 additional_information_bol, pause_each_layer_bol, clean_nozzle_bol, retract_syringe_bol,
                 file_name, storage_path,
                 flow_rate_par_2 = None, pause_each_layer_par_1 = None, pause_each_layer_par_2 = None,
                 clean_nozzle_par_1 = None):

        self.path_to_file = path_to_file

        self.flow_rate_layer_0 = flow_rate_layer_0,
        self.flow_rate_par_1 = flow_rate_par_1
        #flow_rate_differentiate_bol is true if we differentiate the flowrate between outer walls and infill
        self.flow_rate_differentiate_bol = flow_rate_differentiate_bol

        self.bed_temperature = bed_temperature
        self.print_speed = print_speed
        self.fan_bol = fan_bol

        self.additional_information_bol = additional_information_bol
        self.pause_each_layer_bol = pause_each_layer_bol
        self.clean_nozzle_bol = clean_nozzle_bol
        self.retract_syringe_bol = retract_syringe_bol

        self.file_name = file_name
        self.storage_path = storage_path

        self.flow_rate_par_2 = flow_rate_par_2
        self.pause_each_layer_par_1 = pause_each_layer_par_1
        self.pause_each_layer_par_2 = pause_each_layer_par_2
        self.clean_nozzle_par_1 = clean_nozzle_par_1
