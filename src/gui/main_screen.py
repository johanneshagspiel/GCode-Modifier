import os
from tkinter import Frame, Label, Tk, Button, Checkbutton, Entry, StringVar, Radiobutton, filedialog, messagebox, IntVar
import ctypes

from gui.customizations.styles import Styles
from gui.customizations.load_font import load_font
from util.file_handler import File_Handler
from util.command import Command


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
        row_position_index_center_frame += 1

        #File Selection Label
        self.file_selection_label = Label(self.center_frame, text="Which file do you want to modify?", **Styles.label_style_heading)
        self.file_selection_label.grid(row=0, column=0, sticky='nsew')

        #File Selection Frame
        self.file_selection_frame = Frame(self.center_frame, width=720, height=100, background="blue")
        self.file_selection_frame.grid(row=row_position_index_center_frame, column=0, sticky='nsew')
        row_position_index_center_frame += 1
        row_position_index_file_selection_frame = 0

        file_list = []
        file_paths = sorted(self.file_handler.original_gcode_path.glob('*.gcode'))
        for file in file_paths:
            file_list.append(os.path.splitext(file.name)[0])

        self.selected_file = StringVar(self.master, file_list[0])
        list_radio_buttons = []

        for index, file in enumerate(file_list):
            test = Radiobutton(self.file_selection_frame,
                           text=file,
                           variable=self.selected_file,
                           command=self.update_name_selected_file,
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

        default_flow_rate = StringVar(self.print_settings_frame, "55")
        self.flow_rate_entry = Entry(self.print_settings_frame, **Styles.entry_style, textvariable=default_flow_rate)
        self.flow_rate_entry.grid(row=row_position_index_print_settings_frame, column=1, sticky='w')
        row_position_index_print_settings_frame += 1

        #Bed Temperature
        self.bed_temperature_label = Label(self.print_settings_frame, text="Bed Temperature: ",
                                              **Styles.label_style_text)
        self.bed_temperature_label.grid(row=row_position_index_print_settings_frame, column=0, sticky='w')

        default_bed_temperature = StringVar(self.print_settings_frame, "0")
        self.bed_temperature_entry = Entry(self.print_settings_frame, **Styles.entry_style, textvariable=default_bed_temperature)
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
        self.result_add_information = IntVar()
        self.add_information_checkbox = Checkbutton(self.print_modifications_frame, text="Show information while printing",
                                                    variable=self.result_add_information, **Styles.checkbox_style)
        self.add_information_checkbox.grid(row=row_position_index_print_modifications_frame, column=0, sticky='w')
        row_position_index_print_modifications_frame += 1

        #Stop after each layer
        self.stop_afer_each_layer = Checkbutton(self.print_modifications_frame, text="Stop print after each layer", **Styles.checkbox_style)
        self.stop_afer_each_layer.grid(row=row_position_index_print_modifications_frame, column=0, sticky='w')
        row_position_index_print_modifications_frame += 1

        #Retract syringe after end of print
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

        #Name of Modified File
        self.storage_name_label = Label(self.storage_frame, text="Name modified file: ",
                                              **Styles.label_style_text)
        default_text = StringVar(self.storage_frame, value=self.selected_file.get())
        self.storage_name_label.grid(row=row_position_index_storage_frame, column=0, sticky='w')
        self.storage_name_entry = Entry(self.storage_frame, **Styles.entry_style, textvariable=default_text)
        self.storage_name_entry.grid(row=row_position_index_storage_frame, column=1, sticky='w')
        row_position_index_storage_frame += 1

        #Chose Location to store button
        self.storage_location = ""
        self.location_choose_button = Button(self.storage_frame, text="Choose location to store", command=self.select_storage_location,
                                    **Styles.button_style, width=10)
        self.location_choose_button.grid(row=row_position_index_storage_frame, column=0, columnspan=2, sticky='nsew')

        #Location label and entry
        self.path_label = Label(self.storage_frame, text="Storage path: ",
                                        **Styles.label_style_text)
        self.path_name_label = Label(self.storage_frame, text="", **Styles.entry_style)
        self.row_location_storage = row_position_index_storage_frame
        row_position_index_storage_frame += 1

        #Modify Button
        self.modify_button = Button(self.center_frame, text="Modify!", command=self.start_modification, **Styles.button_style, width=10)
        self.modify_button.grid(row=row_position_index_center_frame, column=0, sticky='nsew')

        self.master.lift()  # starts on top of all other applications
        self.master.mainloop()

    def start(self):
        None

    def select_storage_location(self):
        self.storage_location = filedialog.askdirectory()

        new_location = StringVar(self.storage_frame, value=self.storage_location)
        self.path_name_label.configure(textvariable=new_location)

        self.path_label.grid(row=self.row_location_storage, column=0, sticky='w')
        self.path_name_label.grid(row=self.row_location_storage, column=1, sticky='w')
        self.row_location_storage += 1
        self.location_choose_button.grid(row=self.row_location_storage, column=0, columnspan=3, sticky='nsew')
        self.location_choose_button.configure(text="Choose a different location")

    def update_name_selected_file(self):
        new_name = StringVar(self.storage_frame, value=self.selected_file.get())
        self.storage_name_entry.configure(textvariable=new_name)

    def start_modification(self):
        checked = self.sanity_check()

        if checked != False:
            print(checked)

    def sanity_check(self):
        messages = []

        flow_rate = self.flow_rate_entry.get()
        try:
            int_flow_rate = int(flow_rate)
            if int_flow_rate < 10 or int_flow_rate > 400:
                raise Exception
        except Exception:
            messages.append("The flow rate needs to be an integer between 10 and 400.")
            zero_flow_rate = StringVar(self.print_settings_frame, "")
            self.flow_rate_entry.configure(textvariable=zero_flow_rate)

        bed_temperature = self.bed_temperature_entry.get()
        try:
            int_bed_temperature = int(bed_temperature)
            if int_bed_temperature < 0 or int_bed_temperature > 60:
                raise Exception
        except Exception:
            messages.append("The bed temperature needs to be an integer between 0 and 60.")
            zero_bed_temperature = StringVar(self.print_settings_frame, "")
            self.bed_temperature_entry.configure(textvariable=zero_bed_temperature)

        storage_location = self.storage_location
        if len(storage_location) == 0:
            messages.append("A storage location needs to be specified.")

        file_name = self.storage_name_entry.get()
        if len(file_name) == 0:
            messages.append("A filename needs to be specified.")

        if len(messages) > 0:
            error_text = "\n".join(messages)
            messagebox.showerror("Error!", error_text)
            return False

        else:
            stop_each_layer = 0
            retract_syringe_end_of_print = 0
            return Command(flow_rate=int_flow_rate, bed_temperature=int_bed_temperature, add_information=self.result_add_information.get(),
                           stop_each_layer=stop_each_layer, retract_syringe_end_of_print=retract_syringe_end_of_print,
                           file_name=file_name, storage_path=storage_location)
