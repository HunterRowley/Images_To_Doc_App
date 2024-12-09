# https://www.askpython.com/python-modules/tkinter/stringvar-with-examples
import ast
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from ETG_docx import create_doc
from ETG_csv_to_tag import create_tag
from saveDefaultValues import *  # return_template, write_file, read_file, parse_par, conc_par

current_directory = os.getcwd()
default_csv_filename = "Employee ID List"
default_doc_filename = "Operator Tags"

text_template = return_template()


def is_file_present(path):
    file_exists = os.path.exists(path)
    # if filename_message == "":
    #     self.csv_present['text'] = ''
    if file_exists:
        color = "green"
        symbol = u'\u2713'
        response = True
    else:
        color = "red"
        symbol = 'X'
        response = False
    return color, symbol, response


class frame_order_class:
    def __init__(self):
        self.target_directory = 0
        self.csv_filename = 1
        self.doc_filename = 2
        self.picture_size = 3
        self.page_margins = 4
        self.num_tab_stops = 5
        self.tab_stops = 6
        self.spacing = 7
        # self.text_example = 3
        self.buttons = 9
        self.status = self.buttons + 1


frame_order = frame_order_class()

# Limiting the number of inputs for tab_stops
MAX_TAB_STOP_INPUTS = 10

# Parse Par Data Position
#####################
TYPE = 0
POS = 1
#####################
# Margin Limits
UPPER_LIMIT_TB = 10.82
UPPER_LIMIT_LR = 7.83
LOWER_LIMIT_TBLR = 0.0  # 0.17
SPAN_LIMIT_TB = 10.99
SPAN_LIMIT_LR = 8

tab_alignment = [
    'left',
    'center',
    'right'
]

# Any essential parameters for the program that would be read in from the default text file must be added here
default_dict = {'Target Directory':  current_directory,
                'CSV Filename': 'Employee ID List',
                'Doc Name': 'Operator Tags',
                'Picture Width': '2.63',
                'Picture Height': '1.03',
                'Page Margins': "{'top': '', 'bottom': '', 'left': '', 'right': ''}",
                'Tab Stops': '(left,0.14),(center,4.25),(right,8.36)',
                'Line Spacing': '0.0',
                'Test Default': '0.14,4.25,8.36'}


# class margin_warning_window(): #(self, top_bot_error, left_right_error):
#     # https://blog.furas.pl/python-tkinter-how-to-create-popup-window-or-messagebox-gb.html
#     def __init__(self, master):
#         window = tk.Toplevel()
#         message_frame = tk.Frame(window)
#         message_frame.grid(row=0, column=0)
#         button_frame = tk.Frame(window)
#         button_frame.grid(row=1, column=0)
#         # if top_bot_error and left_right_error:
#         #     message = message_top_bot + '\n' + message_left_right
#         # elif top_bot_error:
#         #     message = message_top_bot
#         # elif left_right_error:
#         #     message = message_left_right
#         # else:
#         #     message = "Bad Call"
#
#
#         message_label = tk.Label(message_frame, text=master.page_margin_top_string.get())
#         message_label.grid(column=0, row=0, sticky='WE')
#
#         # tk.Button(button_frame, text='Auto Fix', command=fix_margins).grid(column=0, row=0, sticky='WE')
#         # tk.Button(button_frame, text='Close', command=window.destroy).grid(column=1, row=0, sticky='WE')
#         tk.Button(button_frame, text='Auto Fix').grid(column=0, row=0, sticky='WE')
#         tk.Button(button_frame, text='Close').grid(column=1, row=0, sticky='WE')
#
#     # def retrieve_values():
#     #     top_margin = eval(master.page_margin_top_string.get())
#     #     bot_margin = eval(self.page_margin_bottom_string.get())
#     #     left_margin = eval(self.page_margin_left_string.get())
#     #     right_margin = eval(self.page_margin_right_string.get())
#     #     message_top_bot = f'top margin ({top_margin}") and bottom margin ({bot_margin}") exceed limits'
#     #     message_left_right = f'left margin ({left_margin}") and right margin ({right_margin}") exceed limits'
#     #
#     # def fix_margins(self):
#     #     if top_bot_error:
#     #         self.page_margin_top_string.set(str(round(max(min(10.82, abs(top_margin)), 0.17), 2)))
#     #         self.page_margin_bottom_string.set(str(round(10.99 - float(self.page_margin_top_string.get()), 2)))
#     #     if left_right_error:
#     #         self.page_margin_left_string.set(str(round(max(min(7.83, abs(left_margin)), 0.17), 2)))
#     #         self.page_margin_right_string.set(str(round(8.0 - float(self.page_margin_left_string.get()), 2)))


def is_valid_dict(d):
    if not isinstance(d, dict):
        return False
    for key, value in d.items():
        if not isinstance(key, str):
            return False
        # Add more checks for value types if needed
    for key, value in default_dict.items():
        if not d.__contains__(key):
            d[key] = value
            print(f'added {key} : {d[key]}')
    return True


class TagGeneratorApp(tk.Tk):
    def __init__(self, default=None):
        super().__init__()
        win_h = 440  # 404
        win_w = 402
        self.title('Tag Generator Application')
        # self.geometry(f"{win_w}x{win_h}")  #"500x300")
        # When not defined, tkinter will automatically size the window to the minimum size to fit all the widgets
        self.config(bg="skyblue")
        self.minsize(win_w, win_h)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(frame_order.status, weight=1)

        self.target_directory_frame = tk.Frame(self, width=480, height=100, bg='grey')
        self.target_directory_frame.grid(row=frame_order.target_directory, column=0, padx=10, pady=5, sticky="WE")
        self.target_directory_frame.grid_columnconfigure(1, weight=1)

        self.csv_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.csv_frame.grid(row=frame_order.csv_filename, column=0, padx=10, pady=(5, 0), sticky="SW")

        self.doc_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.doc_frame.grid(row=frame_order.doc_filename, column=0, padx=10, pady=(0, 5), sticky="NW")

        self.pic_size_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.pic_size_frame.grid(row=frame_order.picture_size, column=0, padx=10, pady=5, sticky="W")

        self.page_margin_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.page_margin_frame.grid(row=frame_order.page_margins, column=0, padx=10, pady=5, sticky="W")

        self.num_tab_stop_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.num_tab_stop_frame.grid(row=frame_order.num_tab_stops, column=0, padx=10, pady=(5, 0), sticky="W")

        self.tab_stop_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.tab_stop_frame.grid(row=frame_order.tab_stops, column=0, padx=10, pady=(0, 5), sticky="W")

        self.spacing_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.spacing_frame.grid(row=frame_order.spacing, column=0, padx=10, pady=5, sticky="W")

        self.button_frame = tk.Frame(self, width=400, height=100, bg='grey')
        self.button_frame.grid(row=frame_order.buttons, column=0, padx=10, pady=5)

        self.status_frame = tk.Frame(self, width=400, height=100, bd=1, relief=tk.SUNKEN)
        self.status_frame.grid(row=frame_order.status, column=0, padx=0, pady=0, sticky="SWE")
        self.status_frame.grid_columnconfigure(0, weight=1)

        ################################################################################################################
        # self.parameter = read_file(r'C:\pythonProject\Employee_Tag_Generator\default_value.txt')
        # self.parameter = load_variables_from_textfile(r'C:\pythonProject\Employee_Tag_Generator\default_value.txt')
        try:
            self.parameter = load_variables_from_textfile(current_directory + r'\default_value.txt')
        except FileNotFoundError:
            self.parameter = default_dict

        # Check that all parameters are valid and apply default if they don't exist
        if is_valid_dict(self.parameter):
            self.default = self.parameter
            self.directory_string = tk.StringVar(value=self.parameter['Target Directory'])
            self.csv_string = tk.StringVar(value=self.parameter['CSV Filename'])
            self.doc_name_str = tk.StringVar(value=self.parameter['Doc Name'])
            self.picture_width_string = tk.StringVar(value=self.parameter['Picture Width'])
            self.picture_height_string = tk.StringVar(value=self.parameter['Picture Height'])
            self.space_after_string = tk.StringVar(value=self.parameter['Line Spacing'])
            self.page_margin_pars = ast.literal_eval(self.parameter['Page Margins'])
            # if the value in self.parameter['Page Margins'] is typed out like a dictionary, then ast.literal_eval
            # can safely interpret it as a dictionary
            self.tab_stop_pars = parse_par(self.parameter['Tab Stops'])
        else:
            print("ERROR - Default Parameter Incorrect or Missing")
            self.destroy()

        # Page Margin Parameters
        # for key, value in self.page_margin_pars.items():
        #     print(f'page_margin_pars[{key}] = {value}')
        self.page_margin_top_string = tk.StringVar(value=self.page_margin_pars['top'])
        self.page_margin_bottom_string = tk.StringVar(value=self.page_margin_pars['bottom'])
        self.page_margin_left_string = tk.StringVar(value=self.page_margin_pars['left'])
        self.page_margin_right_string = tk.StringVar(value=self.page_margin_pars['right'])

        # Tab Stop Parameters
        self.tab_stop_type = []
        self.tab_stop_pos = []
        self.num_tab_stop_string = tk.StringVar(value=str(len(self.tab_stop_pars)))

        # --- Not needed since the tab_stop entries remembers previous values when they're called back
        # self.tab_stop_pars_memory = self.tab_stop_pars + [['', '']] * (MAX_TAB_STOP_INPUTS - len(self.tab_stop_pars))

        # --- Make Tab Stop_Pars the max number of inputs but fill the remaining parameters with the value ('','')
        self.tab_stop_pars = self.tab_stop_pars + [['', '']] * (MAX_TAB_STOP_INPUTS - len(self.tab_stop_pars))
        for par in self.tab_stop_pars:
            self.tab_stop_type.append(tk.StringVar(value=par[0]))
            self.tab_stop_pos.append(tk.StringVar(value=par[1]))
        ################################################################################################################

        # Target Directory
        self.directory_label = tk.Label(self.target_directory_frame, text="Target Directory:")
        self.directory_label.grid(column=0, row=0)

        self.directory_entry = tk.Entry(self.target_directory_frame, textvariable=self.directory_string)
        self.directory_entry.grid(column=1, row=0, sticky="WE")
        self.directory_entry.focus()

        # CSV Filename
        self.csv_label = tk.Label(self.csv_frame, text="CSV Filename:", height=1, width=13,
                                  anchor=tk.E)  #text="     CSV Filename:")
        self.csv_label.grid(column=0, row=0)  #(sticky=tk.SE, column=0, row=0)

        self.csv_entry = tk.Entry(self.csv_frame, textvariable=self.csv_string, width=20)
        self.csv_entry.grid(column=1, row=0)  #(sticky=tk.SW, column=1, row=0)
        self.csv_entry.focus()

        self.csv_output_message = tk.Label(self.csv_frame, text=default_csv_filename + ".csv", height=1)
        self.csv_output_message.grid(column=2, row=0)  #(sticky=tk.SE, column=2, row=0)

        default = is_file_present(current_directory + "\\" + default_csv_filename + ".csv")
        self.csv_present = tk.Label(self.csv_frame, text=default[1], height=1)
        self.csv_present.config(fg=default[0])
        self.csv_present.grid(column=3, row=0)  #(sticky=tk.SW, column=3, row=0)

        # self.csv_string.trace('w', self.show_filename) # try lambda here <--------------------------------------
        # With lambda, you need to add some var (a, b, c) to tell lambda how many arguments you're passing through
        # The line below apparently has 3 arguments, hence the 3 variables
        self.csv_string.trace('w', callback=lambda a, b, c: self.show_filename(input_str=self.csv_string,
                                                                               output_str=self.csv_output_message,
                                                                               type_selection=0))

        # Doc Name
        # self.doc_name_label = tk.Label(self.doc_frame, text="Enter Doc Name:")
        self.doc_name_label = tk.Label(self.doc_frame, text="Enter Doc Name:", height=1, width=13, anchor=tk.E)
        self.doc_name_label.grid(sticky="NE", column=0, row=1)

        self.doc_name_entry = tk.Entry(self.doc_frame, textvariable=self.doc_name_str, width=20)
        self.doc_name_entry.grid(sticky="NW", column=1, row=1)
        self.doc_name_entry.focus()

        self.doc_name_message = tk.Label(self.doc_frame, text=default_doc_filename + ".docx", height=1)
        self.doc_name_message.grid(sticky="NW", column=2, row=1)

        self.doc_name_str.trace('w', callback=lambda a, b, c: self.show_filename(input_str=self.doc_name_str,
                                                                                 output_str=self.doc_name_message,
                                                                                 type_selection=1))

        # https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        vcmd_f = (self.register(self.callback_float))
        vcmd_i = (self.register(self.callback_int))

        # Picture Size
        self.pic_width_label = tk.Label(self.pic_size_frame, text="Picture Width", justify='center')
        self.pic_width_label.grid(column=0, row=0, sticky="WE")
        self.pic_height_label = tk.Label(self.pic_size_frame, text="Picture Height", justify='center')
        self.pic_height_label.grid(column=1, row=0, sticky="WE")

        self.pic_width_entry = tk.Entry(self.pic_size_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                        textvariable=self.picture_width_string, justify='center')
        self.pic_width_entry.grid(column=0, row=1)
        self.pic_height_entry = tk.Entry(self.pic_size_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                         textvariable=self.picture_height_string, justify='center')
        self.pic_height_entry.grid(column=1, row=1)

        # Page Margins
        self.page_margin_label = tk.Label(self.page_margin_frame, text="Page Margins")
        self.page_margin_label.grid(sticky="WE", column=0, row=0, columnspan=4)
        self.page_margin_top_label = tk.Label(self.page_margin_frame, text="Top")
        self.page_margin_top_label.grid(sticky="WE", column=0, row=1)
        self.page_margin_bottom_label = tk.Label(self.page_margin_frame, text="Bottom")
        self.page_margin_bottom_label.grid(sticky="WE", column=1, row=1)
        self.page_margin_left_label = tk.Label(self.page_margin_frame, text="Left")
        self.page_margin_left_label.grid(sticky="WE", column=2, row=1)
        self.page_margin_right_label = tk.Label(self.page_margin_frame, text="Right")
        self.page_margin_right_label.grid(sticky="WE", column=3, row=1)

        self.page_margin_top_string.trace('w', callback=lambda a, b, c: self.update_page_margins('top',
                                                                                                 self.page_margin_top_string.get()))
        self.page_margin_bottom_string.trace('w', callback=lambda a, b, c: self.update_page_margins('bottom',
                                                                                                    self.page_margin_bottom_string.get()))
        self.page_margin_left_string.trace('w', callback=lambda a, b, c: self.update_page_margins('left',
                                                                                                  self.page_margin_left_string.get()))
        self.page_margin_right_string.trace('w', callback=lambda a, b, c: self.update_page_margins('right',
                                                                                                   self.page_margin_right_string.get()))
        margin_entry_width = 10
        self.page_margin_top_entry = tk.Entry(self.page_margin_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                              textvariable=self.page_margin_top_string, width=margin_entry_width, justify='center')
        self.page_margin_bottom_entry = tk.Entry(self.page_margin_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                                 textvariable=self.page_margin_bottom_string, width=margin_entry_width, justify='center')
        self.page_margin_left_entry = tk.Entry(self.page_margin_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                               textvariable=self.page_margin_left_string, width=margin_entry_width, justify='center')
        self.page_margin_right_entry = tk.Entry(self.page_margin_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                                textvariable=self.page_margin_right_string, width=margin_entry_width, justify='center')

        self.page_margin_top_entry.grid(column=0, row=2)
        self.page_margin_bottom_entry.grid(column=1, row=2)
        self.page_margin_left_entry.grid(column=2, row=2)
        self.page_margin_right_entry.grid(column=3, row=2)

        # Tab Stops
        self.num_tab_stop_label = tk.Label(self.num_tab_stop_frame, text="No. Tab Stops / Row")
        self.num_tab_stop_label.grid(sticky="WE", column=0, row=0)  #, columnspan=MAX_TAB_STOP_INPUTS)

        self.tab_stop_label = tk.Label(self.tab_stop_frame, text="Tab Stops")
        self.tab_stop_label.grid(sticky="WE", column=0, row=0, columnspan=MAX_TAB_STOP_INPUTS)

        # Moved to above Picture Size
        # # https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        # vcmd_f = (self.register(self.callback))

        self.num_tab_stop_entry = tk.Entry(self.num_tab_stop_frame, validate="all", validatecommand=(vcmd_i, '%P'),
                                           textvariable=self.num_tab_stop_string)
        self.num_tab_stop_entry.configure(width=3, justify='center')
        self.num_tab_stop_entry.grid(sticky="E", column=2, row=0)
        self.num_tab_stop_string.trace('w', callback=lambda a, b, c: self.update_tab_stop_inputs())

        self.tab_stop_pos_entry = []
        self.tab_stop_type_entry = []
        for i in range(0, len(self.tab_stop_pars)):
            self.tab_stop_pos_entry.append(tk.Entry(self.tab_stop_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                                    textvariable=self.tab_stop_pos[i], width=5, justify='center'))
            self.tab_stop_type_entry.append(tk.OptionMenu(self.tab_stop_frame, self.tab_stop_type[i], *tab_alignment))
            self.tab_stop_pos_entry[i].grid(column=i, row=2, sticky="WE")
            self.tab_stop_type_entry[i].grid(column=i, row=3)
            self.tab_stop_type_entry[i].configure(width=4)
            if '' in self.tab_stop_pars[i]:
                self.tab_stop_type_entry[i].grid_remove()
                self.tab_stop_pos_entry[i].grid_remove()

        # Line Spacing
        self.space_after_label = tk.Label(self.spacing_frame, text="Line Spacing")
        self.space_after_label.grid(column=0, row=0, sticky="WE")

        self.space_after_entry = tk.Entry(self.spacing_frame, validate="all", validatecommand=(vcmd_f, '%P'),
                                          textvariable=self.space_after_string, justify='center')
        self.space_after_entry.grid(column=0, row=1)

        # Save Button
        self.save_button = tk.Button(self.button_frame, width=10, text="Save", command=self.clicked_save_doc)
        # lambda allows you to assign a method to the command AND pass arguments to it without executing the method
        # self.save_button = tk.Button(self.button_frame, width=10, text="Save", command=lambda: self.clicked_save_doc(1)) # 1 indicates .docx
        self.save_button.grid(column=0, row=1, padx=5, pady=5, sticky='NESW')

        # Open Doc Button
        self.open_button = tk.Button(self.button_frame, width=10, text="Open", command=self.clicked_open)
        self.open_button.grid(column=1, row=1, padx=5, pady=5, sticky='NESW')

        # Cancel Button
        self.cancel_button = tk.Button(self.button_frame, width=10, text="Cancel", command=self.clicked_cancel)
        # self.cancel_button = tk.Button(self.button_frame, width=10, text="Cancel", command=lambda: print('Cancel'))
        self.cancel_button.grid(column=2, row=1, padx=5, pady=5, sticky='NESW')


        # # Close Doc Button
        # self.close_button= tk.Button(self.button_frame, width=10, text="Close", command=self.clicked_close)
        # self.close_button.grid(column=3, row=1, padx=5, pady=5, sticky='NESW')

        # # Test Read Button
        # self.read_button = tk.Button(self.button_frame, width=10, text="Read", command=self.read_default_values)
        # self.read_button.grid(column=2, row=1, padx=5, pady=5, sticky="NESW")

        # # Test Write Button
        # self.write_button = tk.Button(self.button_frame, width=10, text="Write", command=self.write_default_values)
        # self.write_button.grid(column=3, row=1, padx=5, pady=5, sticky="NESW")
        #
        # # Reset Button
        # self.reset_button = tk.Button(self.button_frame, width=10, text="Reset", command=self.reset_default_values)
        # self.reset_button.grid(column=4, row=1, padx=5, pady=5, sticky="NESW")

        # Status
        self.status_message = tk.Label(self.status_frame, text="Ready", anchor=tk.E)  #, bd=1, relief=tk.SUNKEN)
        self.status_message.grid(sticky='SWE', column=0, row=0)
        # self.status_message.pack(side="bottom", fill="x")
        # self.status_str.trace('w', callback=lambda a, b, c: self.write_status_msg(input_str=self.status_str, output_str=self.status_message, state="normal"))

    def write_callback(self):
        print('The variable has been written to')

    def callback_float(self, P):
        # It doesn't work for floats with the commented code below. It won't take decimal points
        if P == "":
            return True
        else:
            try:
                float(P)
                return True
            except ValueError:
                return False

    def callback_int(self, P):
        # It doesn't work for floats with the commented code below. It won't take decimal points
        if P == "":
            return True
        else:
            try:
                int(P)
                return True
            except ValueError:
                return False

    def create_greeting_message(self, *args):
        name_entered = self.doc_name_str.get()

        greeting_message = ""
        if name_entered != "":
            greeting_message = "Hello " + name_entered

        self.doc_name_message['text'] = greeting_message

    def write_status_msg(self, status, color="black"):
        # state_color = {"normal": "black", "fault": "red", "valid": "green"}
        self.status_message = tk.Label(self.status_frame, text=status, anchor=tk.E)  #, bd=1, relief=tk.SUNKEN)
        self.status_message.config(fg=color)
        self.status_message.grid(sticky='wens', column=0, row=0)

    def show_filename(self, input_str, output_str, type_selection):  #, *args):
        # Not sure how to initialize this value without making it global to the class and declaring it in INIT
        if type(type_selection) != int:
            type_selection = 0

        file_type = {0: ".csv", 1: ".docx", 2: ".jpg", 3: ".png", 4: ".gif", 5: ".txt"}

        entered_filename = input_str.get()
        filename_message = ""
        if entered_filename != "":
            if "." in entered_filename:
                split_filename = entered_filename.split(".")
                if split_filename[1] != file_type[type_selection]:  # Rewrite file type to csv
                    filename_message = split_filename[0] + file_type[type_selection]
                else:
                    filename_message = entered_filename  # The file type is csv and doesn't need changes
            else:
                filename_message = entered_filename + file_type[
                    type_selection]  # Automatically add .csv to the end of entered strings

        output_str['text'] = filename_message
        if file_type[type_selection] == ".csv":
            if filename_message == "":
                output_str['text'] = ''
            else:
                color, symbol, response = is_file_present(
                    self.directory_string.get() + '\\' + self.csv_output_message['text'])
                self.csv_present.config(fg=color)
                self.csv_present['text'] = symbol

    def update_page_margins(self, key, value):
        print('update_page_margins')
        self.page_margin_pars[key] = value

    def update_tab_stop_inputs(self):
        num_tab_stop_string_input = self.num_tab_stop_string.get()
        if num_tab_stop_string_input == "":
            return
        number_inputs = eval(num_tab_stop_string_input)
        if number_inputs > MAX_TAB_STOP_INPUTS:
            self.write_status_msg(f'Max tab_stop input exceeded: {MAX_TAB_STOP_INPUTS}', 'red')
            return
        self.write_status_msg("", "black")
        for i in range(0, number_inputs):
            self.tab_stop_pos_entry[i].grid()
            self.tab_stop_type_entry[i].grid()
            if not self.tab_stop_label.winfo_viewable():
                self.num_tab_stop_frame.grid_configure(pady=(5, 0))
                self.tab_stop_frame.grid()
        for i in range(number_inputs, MAX_TAB_STOP_INPUTS):
            self.tab_stop_type_entry[i].grid_remove()
            self.tab_stop_pos_entry[i].grid_remove()
        if number_inputs == 0:
            self.tab_stop_frame.grid_remove()
            self.num_tab_stop_frame.grid_configure(pady=5)

    def update_tab_stop_pars(self):
        num_tab_stop_string_input = self.num_tab_stop_string.get()
        if num_tab_stop_string_input == "":
            return
        number_inputs = eval(num_tab_stop_string_input)
        for i in range(0, number_inputs):
            self.tab_stop_pars[i] = [self.tab_stop_type[i].get(), self.tab_stop_pos[i].get()]
        for i in range(eval(self.num_tab_stop_string.get()), MAX_TAB_STOP_INPUTS):
            self.tab_stop_pars[i] = ['', '']

    def show_margin_warning_window(self):  #, top_margin, bot_margin, left_margin, right_margin):
        margin_warning_window(self)  #, top_margin, bot_margin, left_margin, right_margin)

    def clicked_save_doc(self, *args):
        pic_w = eval(self.picture_width_string.get())
        pic_h = eval(self.picture_height_string.get())

        # top_str = self.page_margin_top_string.get()
        # bot_str = self.page_margin_bottom_string.get()
        # left_str = self.page_margin_left_string.get()
        # right_str = self.page_margin_right_string.get()

        try:
            top_margin = round(eval(self.page_margin_top_string.get()), 2)
            bot_margin = round(eval(self.page_margin_bottom_string.get()), 2)
            left_margin = round(eval(self.page_margin_left_string.get()), 2)
            right_margin = round(eval(self.page_margin_right_string.get()), 2)
        except SyntaxError:
            top_margin = 0.5
            bot_margin = 0.4
            left_margin = 0.0
            right_margin = 0.0

        # print(f'{LOWER_LIMIT_TBLR <= top_margin <= UPPER_LIMIT_TB = }')
        # print(f'{LOWER_LIMIT_TBLR <= bot_margin <= UPPER_LIMIT_TB = }')
        # print(f'{LOWER_LIMIT_TBLR <= left_margin <= UPPER_LIMIT_LR = }')
        # print(f'{LOWER_LIMIT_TBLR <= right_margin <= UPPER_LIMIT_LR = }')

        top_bot_error = (top_margin + bot_margin) > SPAN_LIMIT_TB
        left_right_error = (left_margin + right_margin) > SPAN_LIMIT_LR
        top_error = top_margin > UPPER_LIMIT_TB or top_margin < LOWER_LIMIT_TBLR
        bot_error = bot_margin > UPPER_LIMIT_TB or bot_margin < LOWER_LIMIT_TBLR
        left_error = left_margin > UPPER_LIMIT_LR or left_margin < LOWER_LIMIT_TBLR
        right_error = right_margin > UPPER_LIMIT_LR or right_margin < LOWER_LIMIT_TBLR
        message = ''

        if top_bot_error:
            message = (
                f'Top Margin ({top_margin}") and Bottom Margin ({bot_margin}") exceed Page Limit ({SPAN_LIMIT_TB}")\n'
                f'{top_margin}" + {bot_margin}" = {top_margin + bot_margin}" > {SPAN_LIMIT_TB}"\n')

        if left_right_error:
            message = (
                    message + f'Left Margin ({left_margin}") and Right Margin ({right_margin}") exceed Page Limit ({SPAN_LIMIT_LR}")\n'
                              f'{left_margin}" + {right_margin}" = {left_margin + right_margin}" > {SPAN_LIMIT_LR}"\n')
        if top_error:
            if top_margin > UPPER_LIMIT_TB:
                message = message + f'Top Margin ({top_margin}") above upper limit {UPPER_LIMIT_TB}"\n'
            if top_margin < LOWER_LIMIT_TBLR:
                message = message + f'Top Margin ({top_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if bot_error:
            if bot_margin > UPPER_LIMIT_TB:
                message = message + f'Bottom Margin ({bot_margin}") above upper limit {UPPER_LIMIT_TB}"\n'
            if bot_margin < LOWER_LIMIT_TBLR:
                message = message + f'Bottom Margin ({bot_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if left_error:
            if left_margin > UPPER_LIMIT_LR:
                message = message + f'Left Margin ({left_margin}") above upper limit {UPPER_LIMIT_LR}"\n'
            if left_margin < LOWER_LIMIT_TBLR:
                message = message + f'Left Margin ({left_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if right_error:
            if right_margin > UPPER_LIMIT_LR:
                message = message + f'Right Margin ({right_margin}") above upper limit {UPPER_LIMIT_LR}"\n'
            if right_margin < LOWER_LIMIT_TBLR:
                message = message + f'Right Margin ({right_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'

        # warning_box = Mbox
        # warning_box.root = self
        # D = {'warning': f'{message}'}
        # b_autofix = tk.Button(self, text='Autofix')
        # b_autofix['command'] = lambda: warning_box(D['warning'])
        # warning_box(msg=message, )
        # return

        if not ((LOWER_LIMIT_TBLR <= top_margin <= UPPER_LIMIT_TB) and (
                LOWER_LIMIT_TBLR <= bot_margin <= UPPER_LIMIT_TB) and
                (LOWER_LIMIT_TBLR <= left_margin <= UPPER_LIMIT_LR) and (
                        LOWER_LIMIT_TBLR <= right_margin <= UPPER_LIMIT_LR) and
                (top_margin + bot_margin) <= SPAN_LIMIT_TB and (left_margin + right_margin) <= SPAN_LIMIT_LR):
            self.show_margin_warning_window()
            return

        dir_str = self.directory_string.get()
        csv_str = self.csv_output_message['text']
        tag_folder_directory = create_tag(dir_str, csv_str)

        # input_tab = []
        # for i in range(0, self.tab_stop_pars):
        #     input_tab.append((self.tab_stop_pars[i][TYPE], self.tab_stop_pars[i][POS]))

        self.update_tab_stop_pars()
        # input_tab = parse_par(conc_par(self.tab_stop_pars))
        # The above is replaced with below, much quicker and easier
        input_tab = []
        add_in = False
        for i in self.tab_stop_pars:
            for j in i:
                if '' != j:
                    add_in = True
                else:
                    add_in = False
            if add_in:
                input_tab.append((i[0], float(i[1])))
                # input_tab entry must start with string denoting the
                # type of tab stop (ie 'left') and following with a float
                # of the position of that tab stop
        # print(input_tab)
        # print(f'{input_tab[0]}, {type(input_tab[0][0])}, {type(input_tab[0][1])}')

        finished = create_doc(tag_folder_directory, self.doc_name_str.get(), top_margin=top_margin,
                              bot_margin=bot_margin, left_margin=left_margin, right_margin=right_margin, tab=input_tab,
                              picture_width=pic_w, picture_height=pic_h,
                              space_after=float(self.space_after_string.get()))
        if finished:
            print('Save Doc Finished')
            self.write_status_msg('Save Doc Finished', 'green')
        else:
            print('Save Doc Failed')
            self.write_status_msg('Save Doc Failed', 'red')

    def clicked_open(self, *args):
        self.write_status_msg('', 'black')
        doc_path = self.directory_string.get() + '\\' + self.doc_name_message['text']
        color, symbol, response = is_file_present(doc_path)
        if response:
            os.startfile(self.directory_string.get() + '\\' + self.doc_name_message['text'])
        else:
            self.write_status_msg(f'File not found: {doc_path}', 'red')

    def clicked_cancel(self, *args):
        print('clicked_Cancel')
        # self.status_str.set("Clicked Cancel")
        # self.status_str = 'Clicked Cancel'
        self.write_status_msg('Clicked Cancel', 'black')
        self.destroy()


    # def clicked_close(self, *args):
    #     print('clicked close doc')
    #     os. (self.doc_name_str.get())

    # def read_default_values(self):
    #     parameter = read_file('C:\pythonProject\Employee_Tag_Generator\default_value.txt')
    #     # print(parameter)
    #     if parameter[0][1] != '': self.directory_string.set(parameter[0][1])
    #     if parameter[1][1] != '': self.csv_string.set(parameter[1][1])
    #     if parameter[2][1] != '': self.doc_name_str.set(parameter[2][1])
    #     if parameter[3][1] != '': self.picture_width_string.set(parameter[3][1])
    #     if parameter[4][1] != '': self.picture_height_string.set(parameter[4][1])
    #     if parameter[5][1] != '': self.left_tab_stop_string.set(parameter[5][1])
    #     if parameter[6][1] != '': self.center_tab_stop_string.set(parameter[6][1])
    #     if parameter[7][1] != '': self.right_tab_stop_string.set(parameter[7][1])
    #     if parameter[8][1] != '': self.space_after_string.set(parameter[8][1])

    def write_default_values(self):
        # parameter = []
        # parameter.append((text_template[0], self.directory_string.get()))
        # parameter.append((text_template[1], self.csv_string.get()))
        # parameter.append((text_template[2], self.doc_name_str.get()))
        # parameter.append((text_template[3], self.picture_width_string.get()))
        # parameter.append((text_template[4], self.picture_height_string.get()))
        # parameter.append((text_template[5], self.left_tab_stop_string.get()))
        # parameter.append((text_template[6], self.center_tab_stop_string.get()))
        # parameter.append((text_template[7], self.right_tab_stop_string.get()))
        # parameter.append((text_template[8], self.space_after_string.get()))
        #
        # write_file('C:\pythonProject\Employee_Tag_Generator\default_value.txt', parameter)

        # Separate test from above function --------------------------------------------------------------------------------
        # input_tab = [(float(self.left_tab_stop_string.get()), 'left'), (float(self.center_tab_stop_string.get()), 'center'),
        #              (float(self.right_tab_stop_string.get()), 'right')]
        # for pos in self.tab_stop_pos:
        #     print(pos.get())
        # for typ in self.tab_stop_type:
        #     print(typ.get())
        default_tab_stop = []

        for i in range(0, eval(self.num_tab_stop_string.get())):
            self.tab_stop_pars[i] = [self.tab_stop_type[i].get(), self.tab_stop_pos[i].get()]
            if self.tab_stop_type[i].get() != '' and self.tab_stop_pos[i].get() != '':
                default_tab_stop.append(self.tab_stop_pars[i])
        print(default_tab_stop)

    def save_default_values_and_exit(self):

        self.parameter['Target Directory'] = self.directory_string.get()
        self.parameter['CSV Filename'] = self.csv_string.get()
        self.parameter['Doc Name'] = self.doc_name_str.get()
        self.parameter['Picture Width'] = self.picture_width_string.get()
        self.parameter['Picture Height'] = self.picture_height_string.get()
        self.parameter['Page Margins'] = str(self.page_margin_pars)
        self.parameter['Test Default'] = '0.14,4.25,8.36'
        self.parameter['Line Spacing'] = self.space_after_string.get()

        ###############################################################################################
        # # When type and pos are updated through the GUI, update tab_stop_pars through their string trace callback instead of updating it here
        # for i in range(0, eval(self.num_tab_stop_string.get())):
        #     self.tab_stop_pars[i] = [self.tab_stop_type[i].get(), self.tab_stop_pos[i].get()]
        # for i in range(eval(self.num_tab_stop_string.get()), MAX_TAB_STOP_INPUTS):
        #     self.tab_stop_pars[i] = ['', '']
        self.update_tab_stop_pars()
        self.parameter['Tab Stops'] = conc_par(self.tab_stop_pars)
        ###############################################################################################

        write_variables_to_textfile(current_directory + r'\default_value.txt', self.parameter)

        self.destroy()

    def consolidate_tab_stop_pars(self):
        temp_pars = []
        for i in range(0, len(self.tab_stop_pars)):
            if self.tab_stop_type[i].get() != '' and self.tab_stop_pos[i].get() != '':
                temp_pars.append(self.tab_stop_pars[i])
        print(temp_pars)

    def reset_default_values(self):

        self.directory_string.set(self.default['Target Directory'])
        self.csv_string.set(self.default['CSV Filename'])
        self.doc_name_str.set(self.default['Doc Name'])
        self.picture_width_string.set(self.default['Picture Width'])
        self.picture_height_string.set(self.default['Picture Height'])
        self.space_after_string.set(self.default['Line Spacing'])

        self.tab_stop_str = []
        for string in self.default['Tab Stops']:
            self.tab_stop_str.append(tk.StringVar(value=string))

    # def Frame(self, self1, width, height, bg):
    #     pass


class margin_warning_window():  # (self, top_bot_error, left_right_error):
    # https://blog.furas.pl/python-tkinter-how-to-create-popup-window-or-messagebox-gb.html
    def __init__(self, master):
        self.master = master
        self.window = tk.Toplevel()
        self.window.config(bg='skyblue')
        self.message_frame = tk.Frame(self.window)
        self.message_frame.grid(row=0, column=0)
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=1, column=0)

        self.test_frame = tk.Frame(self.window)
        self.test_frame.configure(bg='lightgreen')
        self.test_frame.grid(row=2, column=0)

        # words = ["You", "Done", "F*cked", "Up"]
        # colours = ["blue", "green", "red", "yellow"]
        #
        # for index, word in enumerate(words):
        #     tk.Label(self.test_frame, text=word, fg=colours[index]).grid(column=index, row=0)

        self.retrieve_values()

        # Height of sheet is 11" and needs 0.01" minimum difference between margins
        # Width of sheet is 8.5" and needs 0.5" minimum difference between margins
        # Top and Bottom have a max value of 10.82"
        # Left and Right have a max value of 7.83"
        # All margins have a minimum of 0.17" CONTINUED BELOW
        # Turns out, you can set the margins to 0. Word will open the document with 0 margin
        # When you open the margin menu, it'll then issue a warning that the minimum needs to be 0.17"
        ### Margin Limits ###
        # UPPER_LIMIT_TB = 10.82
        # UPPER_LIMIT_LR = 7.83
        # LOWER_LIMIT_TBLR = 0.17
        # SPAN_LIMIT_TB = 10.99
        # SPAN_LIMIT_LR = 8
        self.top_bot_error = (self.top_margin + self.bot_margin) > SPAN_LIMIT_TB
        self.left_right_error = (self.left_margin + self.right_margin) > SPAN_LIMIT_LR
        self.top_error = self.top_margin > UPPER_LIMIT_TB or self.top_margin < LOWER_LIMIT_TBLR
        self.bot_error = self.bot_margin > UPPER_LIMIT_TB or self.bot_margin < LOWER_LIMIT_TBLR
        self.left_error = self.left_margin > UPPER_LIMIT_LR or self.left_margin < LOWER_LIMIT_TBLR
        self.right_error = self.right_margin > UPPER_LIMIT_LR or self.right_margin < LOWER_LIMIT_TBLR

        # #---------- OLD ----------
        # self.message = ''
        # self.update_message_OLD()
        # message_label = tk.Label(self.test_frame, text=self.message)
        # message_label.configure(bg='aqua')
        # message_label.grid(column=0, row=0, sticky='WE')
        # # ---------- OLD ----------

        # tk.Button(button_frame, text='Auto Fix', command=fix_margins).grid(column=0, row=0, sticky='WE')
        # tk.Button(button_frame, text='Close', command=window.destroy).grid(column=1, row=0, sticky='WE')
        tk.Button(button_frame, text='Auto Fix', command=self.fix_margins).grid(column=0, row=0, padx=5, pady=5,
                                                                                sticky='WE')
        tk.Button(button_frame, text='Close', command=self.window.destroy).grid(column=1, row=0, padx=5, pady=5,
                                                                                sticky='WE')

        if self.top_bot_error:
            top_bot_error_msg = [('Top margin (', 'black'),
                                 (f'{self.top_margin}"', 'red'),
                                 (') and Bottom Margin (', 'black'),
                                 (f'{self.bot_margin}"', 'red'),
                                 (') exceed Page Limit (', 'black'),
                                 (f'{UPPER_LIMIT_TB}"', 'blue'),
                                 (')', 'black')]
            self.update_message(warning_msg=top_bot_error_msg)
            top_bot_equation_msg = [(
                                    f'{self.top_margin}" + {self.bot_margin}" = {self.top_margin + self.bot_margin}" > {SPAN_LIMIT_TB}"',
                                    'black')]
            self.update_message(warning_msg=top_bot_equation_msg)
        if self.left_right_error:
            left_right_error_msg = [('Left Margin (', 'black'),
                                    (f'{self.left_margin}"', 'red'),
                                    (') and Right Margin (', 'black'),
                                    (f'{self.right_margin}"', 'red'),
                                    (') exceed Page Limit (', 'black'),
                                    (f'{SPAN_LIMIT_LR}"', 'blue'),
                                    (')', 'black')]
            self.update_message(warning_msg=left_right_error_msg)
            left_right_equation_msg = [(
                                       f'{self.left_margin}" + {self.right_margin}" = {self.left_margin + self.right_margin}" > {SPAN_LIMIT_LR}"',
                                       'black')]
            self.update_message(warning_msg=left_right_equation_msg)
        if self.top_error:
            top_error_msg = [('Top Margin (', 'black'),
                             (f'{self.top_margin}"', 'red')]
            if self.top_margin > UPPER_LIMIT_TB:
                top_error_msg.append((') above upper limit ', 'black'))
                top_error_msg.append((f'{UPPER_LIMIT_TB}"', 'blue'))
            else:
                top_error_msg.append((') below lower limit ', 'black'))
                top_error_msg.append((f'{LOWER_LIMIT_TBLR}"', 'blue'))
            self.update_message(warning_msg=top_error_msg)
        if self.bot_error:
            bot_error_msg = [('Bottom Margin (', 'black'),
                             (f'{self.bot_margin}"', 'red')]
            if self.top_margin > UPPER_LIMIT_TB:
                bot_error_msg.append((') above upper limit ', 'black'))
                bot_error_msg.append((f'{UPPER_LIMIT_TB}"', 'blue'))
            else:
                bot_error_msg.append((') below lower limit ', 'black'))
                bot_error_msg.append((f'{LOWER_LIMIT_TBLR}"', 'blue'))
            self.update_message(warning_msg=bot_error_msg)
        if self.left_error:
            left_error_msg = [('Left Margin (', 'black'),
                              (f'{self.left_margin}"', 'red')]
            if self.top_margin > UPPER_LIMIT_TB:
                left_error_msg.append((') above upper limit ', 'black'))
                left_error_msg.append((f'{UPPER_LIMIT_LR}"', 'blue'))
            else:
                left_error_msg.append((') below lower limit ', 'black'))
                left_error_msg.append((f'{LOWER_LIMIT_TBLR}"', 'blue'))
            self.update_message(warning_msg=left_error_msg)
        if self.right_error:
            right_error_msg = [('Right Margin (', 'black'),
                               (f'{self.right_margin}"', 'red')]
            if self.top_margin > UPPER_LIMIT_TB:
                right_error_msg.append((') above upper limit ', 'black'))
                right_error_msg.append((f'{UPPER_LIMIT_LR}"', 'blue'))
            else:
                right_error_msg.append((') below lower limit ', 'black'))
                right_error_msg.append((f'{LOWER_LIMIT_TBLR}"', 'blue'))
            self.update_message(warning_msg=right_error_msg)

    def retrieve_values(self):
        self.top_margin = eval(self.master.page_margin_top_string.get())
        self.bot_margin = eval(self.master.page_margin_bottom_string.get())
        self.left_margin = eval(self.master.page_margin_left_string.get())
        self.right_margin = eval(self.master.page_margin_right_string.get())

    def update_message_OLD(self):
        if self.top_bot_error:
            self.message = (
                f'Top Margin ({self.top_margin}") and Bottom Margin ({self.bot_margin}") exceed Page Limit ({SPAN_LIMIT_TB}")\n'
                f'{self.top_margin}" + {self.bot_margin}" = {self.top_margin + self.bot_margin}" > {SPAN_LIMIT_TB}"\n')

        if self.left_right_error:
            self.message = (
                    self.message + f'Left Margin ({self.left_margin}") and Right Margin ({self.right_margin}") exceed Page Limit ({SPAN_LIMIT_LR}")\n'
                                   f'{self.left_margin}" + {self.right_margin}" = {self.left_margin + self.right_margin}" > {SPAN_LIMIT_LR}"\n')
        if self.top_error:
            if self.top_margin > UPPER_LIMIT_TB:
                self.message = self.message + f'Top Margin ({self.top_margin}") above upper limit {UPPER_LIMIT_TB}"\n'
            if self.top_margin < LOWER_LIMIT_TBLR:
                self.message = self.message + f'Top Margin ({self.top_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if self.bot_error:
            if self.bot_margin > UPPER_LIMIT_TB:
                self.message = self.message + f'Bottom Margin ({self.bot_margin}") above upper limit {UPPER_LIMIT_TB}"\n'
            if self.bot_margin < LOWER_LIMIT_TBLR:
                self.message = self.message + f'Bottom Margin ({self.bot_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if self.left_error:
            if self.left_margin > UPPER_LIMIT_LR:
                self.message = self.message + f'Left Margin ({self.left_margin}") above upper limit {UPPER_LIMIT_LR}"\n'
            if self.left_margin < LOWER_LIMIT_TBLR:
                self.message = self.message + f'Left Margin ({self.left_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'
        if self.right_error:
            if self.right_margin > UPPER_LIMIT_LR:
                self.message = self.message + f'Right Margin ({self.right_margin}") above upper limit {UPPER_LIMIT_LR}"\n'
            if self.right_margin < LOWER_LIMIT_TBLR:
                self.message = self.message + f'Right Margin ({self.right_margin}") below lower limit {LOWER_LIMIT_TBLR}"\n'

    def update_message(self, warning_msg):
        self.canvas = tk.Canvas(self.message_frame)
        self.canvas.pack(anchor='w')
        y = 10
        x = 5
        for i, (msg, color) in enumerate(warning_msg):
            self.canvas.create_text(x, y, text=msg, fill=color, anchor='w')
            x = self.canvas.bbox('all')[2]
        self.canvas.configure(width=self.canvas.bbox('all')[2], height=self.canvas.bbox('all')[3])

    def fix_margins(self):
        ### Margin Limits ###
        # UPPER_LIMIT_TB = 10.82
        # UPPER_LIMIT_LR = 7.83
        # LOWER_LIMIT_TBLR = 0.17
        # SPAN_LIMIT_TB = 10.99 # 0.01 less than 11
        # SPAN_LIMIT_LR = 8 # 0.5 less than 8.5

        if self.top_bot_error:
            self.master.page_margin_top_string.set(
                str(round(max(min(UPPER_LIMIT_TB, abs(self.top_margin)), LOWER_LIMIT_TBLR), 2)))
            self.master.page_margin_bottom_string.set(
                str(round(SPAN_LIMIT_TB - float(self.master.page_margin_top_string.get()), 2)))
            self.top_bot_error = False
            self.top_error = False
            self.bot_error = False
        if self.left_right_error:
            self.master.page_margin_left_string.set(
                str(round(max(min(UPPER_LIMIT_LR, abs(self.left_margin)), LOWER_LIMIT_TBLR), 2)))
            self.master.page_margin_right_string.set(
                str(round(SPAN_LIMIT_LR - float(self.master.page_margin_left_string.get()), 2)))
            self.left_right_error = False
            self.left_error = False
            self.right_error = False
        if self.top_error:
            if self.top_margin > UPPER_LIMIT_TB:
                self.master.page_margin_top_string.set(str(UPPER_LIMIT_TB))
            if self.top_margin < LOWER_LIMIT_TBLR:
                self.master.page_margin_top_string.set(str(LOWER_LIMIT_TBLR))
            self.top_error = False
        if self.bot_error:
            if self.bot_margin > UPPER_LIMIT_TB:
                self.master.page_margin_bottom_string.set(str(UPPER_LIMIT_TB))
            if self.bot_margin < LOWER_LIMIT_TBLR:
                self.master.page_margin_bottom_string.set(str(LOWER_LIMIT_TBLR))
            self.bot_error = False
        if self.left_error:
            if self.left_margin > UPPER_LIMIT_LR:
                self.master.page_margin_left_string.set(str(UPPER_LIMIT_LR))
            if self.left_margin < LOWER_LIMIT_TBLR:
                self.master.page_margin_left_string.set(str(LOWER_LIMIT_TBLR))
            self.left_error = False
        if self.right_error:
            if self.right_margin > UPPER_LIMIT_LR:
                self.master.page_margin_right_string.set(str(UPPER_LIMIT_LR))
            if self.right_margin < LOWER_LIMIT_TBLR:
                self.master.page_margin_right_string.set(str(LOWER_LIMIT_TBLR))
            self.right_error = False

        self.master.write_status_msg('Retry Save Document')
        self.window.destroy()


if __name__ == "__main__":
    app = TagGeneratorApp()
    app.protocol("WM_DELETE_WINDOW", app.save_default_values_and_exit)
    app.mainloop()
    # print(u'\u2713') # Checkmark
