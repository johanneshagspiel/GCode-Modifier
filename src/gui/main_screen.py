from pathlib import Path
from tkinter import Frame, Label, Tk, Button, Checkbutton, Entry, StringVar, IntVar, Radiobutton, W
import ctypes

from gui.customizations.styles import Styles
from gui.customizations.load_font import load_font
from util.file_handler import File_Handler


class MainScreen:

    def __init__(self):
        self.master = Tk()
        self.file_handler = File_Handler()

        program_name="Paste Printer G-code Modifier - Version "
        program_version ="0.1"

        self.master.title(program_name + program_version)
        self.master.geometry("%dx%d+%d+%d" % (720, 720, 160, 56))
        self.master.resizable(width=False, height=False)

        #updates the taskbar icon
        myappid =program_name + program_version # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #updates the application window icon
        self.master.iconbitmap(True, self.file_handler.used_icon_path)

        #loads custom font
        load_font(self.file_handler.used_font_path)
        row_position_index_center_frame = 0

        self.center_frame = Frame(self.master, width=720, height=720, background="grey")
        self.center_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        #self.center_frame.grid_propagate(0)
        row_position_index_center_frame += 1

        #File Selection Label
        self.file_selection_label = Label(self.center_frame, text="Which file do you want to modify?", **Styles.label_style_heading)
        self.file_selection_label.grid(row=0, column=0, sticky='nsew')

        #File Selection Frame
        self.file_selection_frame = Frame(self.center_frame, width=720, height=100, background="blue")
        self.file_selection_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        #self.file_selection_frame.grid_propagate(0)
        row_position_index_center_frame += 1
        row_position_index_file_selection_frame = 0

        file_list = []
        file_paths = sorted(self.file_handler.original_gcode_path.glob('*.gcode'))
        for file in file_paths:
            file_list.append(file.name)

        self.selected_file = StringVar(self.master, file_list[0])
        # self.selected_file.set(0)
        list_radio_buttons = []

        for index, file in enumerate(file_list):
            test = Radiobutton(self.file_selection_frame,
                           text=file,
                           variable=self.selected_file,
                           **Styles.checkbox_style,
                           value=file)
            test.grid(row=index, column=0, sticky="w")
            list_radio_buttons.append(test)


        #Print setting label
        self.print_settings_label = Label(self.center_frame, text="Which print settings do you want to use?",
                                              **Styles.label_style_heading)
        self.print_settings_label.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1

        #Print_Settings_Frame
        self.print_settings_frame = Frame(self.center_frame, width=700, height=200, background="green")
        self.print_settings_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1
        row_position_index_print_settings_frame = 0

        #Flow Rate
        self.flow_rate_label = Label(self.print_settings_frame, text="Flow rate: ",
                                              **Styles.label_style_text)
        self.flow_rate_label.grid(row=row_position_index_print_settings_frame, column=0, sticky='w')
        self.flow_rate_entry = Entry(self.print_settings_frame, **Styles.entry_style)
        self.flow_rate_entry.grid(row=row_position_index_print_settings_frame, column=1, sticky='w')
        row_position_index_print_settings_frame += 1

        # #Bed Temperature
        self.bed_temperature_label = Label(self.print_settings_frame, text="Bed Temperature: ",
                                              **Styles.label_style_text)
        self.bed_temperature_label.grid(row=row_position_index_print_settings_frame, column=0, sticky='w')
        self.bed_temperature_entry = Entry(self.print_settings_frame, **Styles.entry_style)
        self.bed_temperature_entry.grid(row=row_position_index_print_settings_frame, column=1, sticky='w')
        row_position_index_print_settings_frame += 1

        #Modification Label
        self.print_modifications_label = Label(self.center_frame, text="What do you want to modify?",
                                              **Styles.label_style_heading)
        self.print_modifications_label.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1

        # Print_Modifications_Frame
        self.print_modifications_frame = Frame(self.center_frame, width=720, height=200, background="black")
        self.print_modifications_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1
        row_position_index_print_modifications_frame = 0

        #Add Information
        self.add_information_checkbox = Checkbutton(self.print_modifications_frame, text="Show information while printing", **Styles.checkbox_style)
        self.add_information_checkbox.grid(row=row_position_index_print_modifications_frame, column=0, sticky='w')
        row_position_index_print_modifications_frame += 1

        #Stop after each layer
        self.stop_afer_each_layer = Checkbutton(self.print_modifications_frame, text="Stop print after each layer", **Styles.checkbox_style)
        self.stop_afer_each_layer.grid(row=row_position_index_print_modifications_frame, column=0, sticky='w')
        row_position_index_print_modifications_frame += 1

        #Stop after each layer
        self.retract_syringe_end_of_print = Checkbutton(self.print_modifications_frame, text="Retract the syringe at the end of print", **Styles.checkbox_style)
        self.retract_syringe_end_of_print.grid(row=row_position_index_print_modifications_frame, column=0, sticky='w')
        row_position_index_print_modifications_frame += 1

        # Storage Label
        self.storage_label = Label(self.center_frame, text="How do you want to store the file?",
                                               **Styles.label_style_heading)
        self.storage_label.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1

        # Storage Frame
        self.storage_frame = Frame(self.center_frame, width=720, height=200, background="red")
        self.storage_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1
        row_position_index_storage_frame = 0

        # Storage Name
        self.storage_name_label = Label(self.storage_frame, text="Name modified file: ",
                                              **Styles.label_style_text)
        default_text = StringVar(self.storage_frame, value=self.selected_file.get())
        self.storage_name_label.grid(row=row_position_index_storage_frame, column=0, sticky='w')
        self.storage_name_entry = Entry(self.storage_frame, **Styles.entry_style, textvariable=default_text)
        self.storage_name_entry.grid(row=row_position_index_storage_frame, column=1, sticky='w')
        row_position_index_storage_frame += 1

        #Location Button
        self.location_choose_button = Button(self.center_frame, text="Choose location to store", command=None,
                                    **Styles.button_style, width=10)
        self.location_choose_button.grid(row=row_position_index_storage_frame, column=0, sticky='nsew')

        #Modify Button
        self.modify_button = Button(self.center_frame, text="Modify!", command=self.start_modification, **Styles.button_style, width=10)
        self.modify_button.grid(row=row_position_index_center_frame, column=0, sticky='nsew')

        self.master.lift()  # starts on top of all other applications
        self.master.mainloop()

    def start(self):
        None

    def start_modification(self):
        print(self.selected_file.get())

