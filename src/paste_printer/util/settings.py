
class Settings():

    def __init__(self, environment, big_syringe):
        self.environment = environment
        self.big_syringe = big_syringe

class Environment():

    def __init__(self, printer, sponge):
        self.printer = printer
        self.sponge = sponge

class Printer():

    def __init__(self, bed_width_x, bed_depth_y, height_z):
        self.bed_width_x = bed_width_x
        self.bed_depth_y = bed_depth_y
        self.height_z = height_z

class Sponge():

    def __init__(self, width_x, depth_y, height_z):
        self.width_x = width_x
        self.depth_y = depth_y
        self.height_z = height_z

class Big_Syringe():

    def __init__(self, flow_rate_modifier):
        self.flow_rate_modifier = flow_rate_modifier
