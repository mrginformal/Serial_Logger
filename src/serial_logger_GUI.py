import serial
import serial.tools.list_ports
import pandas as pd
import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import sys
import threading as th
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import math
import ast
import time


class APP(ctk.CTk):
    def __init__(self):

        super().__init__()
        ctk.set_appearance_mode('Dark')
        mplstyle.use('fast')

        ############## configure application window
        self.title('Serial Logger')
        self.scrn_w = self.winfo_screenwidth() - 100
        self.scrn_h = self.winfo_screenheight() - 100
        self.config(background='black')
        self.geometry(f'{self.scrn_w}x{self.scrn_h}+50+25')
        self.grid_rowconfigure(0, weight=0, minsize=250)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure(0, weight=14)
        self.grid_columnconfigure(1, weight=1)

        self.protocol("WM_DELETE_WINDOW", self._quit)
    

        ############## Application variables
        self.font1 = ctk.CTkFont(family='Arial Baltic', size=20, weight='bold')
        self.font2 = ctk.CTkFont(family='Arial Baltic', size=14, weight='bold')
        
        self.text_filename = ctk.StringVar(value='FilePath:                        ')
        self.port_selection =  ctk.StringVar(value='Select')
        
        self.port_names = [str(p.device) for p in serial.tools.list_ports.comports()]
        self.start_button_state = True
        self.is_valid_filename = False

        self.time_map = {'1 min' : 60,
                    '5 min': 300,
                    '30 min' : 1800,
                    '1 hour': 3600,
                    'ShowMeTheData' : None}
        
        self.graphing_interval = ctk.StringVar(value='5 min')
        

        ############## selections frame
        self.selection_frame = ctk.CTkScrollableFrame(self, corner_radius=5, bg_color='black', fg_color='grey18')
        self.selection_frame.grid(row=0, column=0, padx=(10,5), pady=(5,0), sticky='nsew')
        self.selection_frame.columnconfigure((0,1,2,3,4), weight=1)


        ############## Graph Frame
        self.graph_frame = ctk.CTkFrame(self, corner_radius=0, bg_color='black', fg_color='grey18')
        self.graph_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky='nsew')
        self.graph_frame.rowconfigure(0, weight=1)
        self.graph_frame.columnconfigure(0, weight=1)
         
        plt.style.use('dark_background') 

        fig1, ax1 = plt.subplots()
        plt.grid(color='.5')
        plt.subplots_adjust(left=.04, right=.83, top=.95, bottom=.08)
        self.fig1 = fig1
        self.ax1 = ax1
        self.ax1.spines[['top', 'bottom', 'left', 'right']].set_color('0.18')
        self.ax1.spines[['top', 'bottom', 'left', 'right']].set_linewidth(4)
        self.ax1.xaxis.label.set_color('.5')
        self.ax1.yaxis.label.set_color('.5')
        self.ax1.grid(False)

        self.ax1.tick_params(axis='both', width=3, colors='.5', which='both', size=10)

        self.canvas1 = FigureCanvasTkAgg(self.fig1, self.graph_frame)
        self.canvas1.get_tk_widget().grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.canvas1.draw()


        ############# Options Frame
        self.options_frame = ctk.CTkFrame(self, corner_radius=5, bg_color='black', fg_color='grey18')
        self.options_frame.grid(row=0, column=1, padx=(5,10), pady=(5,0), sticky='nsew')
        self.options_frame.columnconfigure(0, weight=1)
        self.options_frame.rowconfigure((0,1,2,3,4,5,6), weight=1)
        
        self.save_as_button = ctk.CTkButton(self.options_frame, corner_radius=5, text='SaveAs', fg_color='yellow2', text_color='grey18', font=self.font1, text_color_disabled='black', command=self.get_filename, hover_color='grey50')
        self.save_as_button.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.file_path_label = ctk.CTkLabel(self.options_frame, corner_radius=5, textvariable=self.text_filename, fg_color='black', text_color='yellow2', font=self.font2, width=200)
        self.file_path_label.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.port_label = ctk.CTkLabel(self.options_frame, corner_radius=5, text='Port', fg_color='grey18', text_color='yellow2', font=self.font1)
        self.port_label.grid(row=2, column=0, padx=5, pady=0, sticky='nsew')
        self.port_menu = ctk.CTkOptionMenu(self.options_frame, values=self.port_names, variable=self.port_selection, button_color='black', dropdown_hover_color='grey50', button_hover_color='grey50', dropdown_font=self.font2, text_color='yellow2', dropdown_text_color='yellow2', dropdown_fg_color='black', font=self.font2, fg_color='black')
        self.port_menu.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
        
        self.interval_label = ctk.CTkLabel(self.options_frame, corner_radius=5, text='Graphing Interval', fg_color='grey18', text_color='yellow2', font=self.font1)
        self.interval_label.grid(row=4, column=0, padx=5, pady=0, sticky='nsew')
        self.port_menu = ctk.CTkOptionMenu(self.options_frame, values=list(self.time_map.keys()), variable=self.graphing_interval, button_color='black', dropdown_hover_color='grey50', button_hover_color='grey50', dropdown_font=self.font2, text_color='yellow2', dropdown_text_color='yellow2', dropdown_fg_color='black', font=self.font2, fg_color='black')
        self.port_menu.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

        self.start_button = ctk.CTkButton(self.options_frame, corner_radius=5, text='Start', fg_color='yellow2', text_color='grey18', command=self.log_data, font=self.font1, hover_color='grey50')
        self.start_button.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')


    def log_data(self):

        if self.start_button_state: # they clicked the start button

            try:
                # Verify valid inputs, then disable inputs so they can't change
                if not self.is_valid_filename:
                    raise ValueError('No valid Filename selected')
                
                if not self.port_names:
                    raise ValueError('No Ports detected')

                self.port_menu.configure(state='disabled')
                self.save_as_button.configure(state='disabled', fg_color='grey50')

                # Open serial port and get data to create graph buttons, make the buttons, close and reopen the port to clear buffers
                self.open_port = serial.Serial(port=self.port_selection.get(), baudrate=115200, timeout=10)

                initial_data = self.read_data(self.open_port, time.time())
                self.parameter_selections = {}
                self.data_table = None
                self.graph_table = None

                self.open_port.close()
                for i, label in enumerate(initial_data):
                    button = ctk.CTkCheckBox(self.selection_frame, text=label, corner_radius=10, checkbox_width=50, hover_color='grey50', border_color='black', fg_color='black', border_width=3)
                    button.grid(row=math.floor(i/5), column=i%5, padx=5, pady=5, sticky='nsew')
                    self.parameter_selections[label] = button
                
                self.open_port.open()

                # open thread which setsup and handles the data processing/graphing loop
                plotting_thread = th.Thread(target=self.plot_data, daemon=True)

                self.stop_flag = th.Event()
                self.lock = th.Lock()

                plotting_thread.start()
            
                #change the start button to a stop button, and changed the flag to false so the next time you press it will exit the program
                self.start_button_state = False
                self.start_button.configure(text='Stop')

    
            except Exception as err:
                # any errors will get a popup window, to tell you that you have incorrect inputs, or what ever else goes wrong
                message_box = tk.Toplevel(self)
                message_box.configure(background='grey50')
                message_box.title('Error Message')
                message_box.geometry(f'300x150+{(int(self.winfo_screenwidth()/2) - 150)}+{(int(self.winfo_screenheight()/2) - 75)}')
                textbox = ctk.CTkTextbox(message_box, corner_radius=5, text_color='black', bg_color='grey50', fg_color='grey50', wrap='word')
                textbox.insert("0.0", err)
                textbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
            
        else:   # they clicked the stop button
            
            # stop the graphing thread, save data and generate a test comeplete message.
            self.stop_flag.set()

            if self.filename.is_file(): 
                self.save(header=False)
            else:
                self.save()
            
            self.complete_message()

    def plot_data(self):

        #Generate a empty line object for every detected parameter
        self.lines = {}
        for param in self.parameter_selections:
            line, = self.ax1.plot([],[])
            self.lines[param] = line

        start_time = time.time()

        while True:
            if self.stop_flag.is_set():
                break
            
            try:
                data = self.read_data(self.open_port, start_time)

                # if the new line has differnt keys(aka parameter like a new tank added or removed) it will delete old buttons and generate new buttons

                if self.parameter_selections.keys() != data.keys():

                    self.parameter_selections = {}

                    for widget in self.selection_frame.winfo_children():              #all existing buttons need to be deleted before making the new ones, but we only want to delete the buttons
                        if isinstance(widget, (ctk.CTkCheckBox)):
                            widget.destroy()

                    for i, label in enumerate(data):
                        button = ctk.CTkCheckBox(self.selection_frame, text=label, corner_radius=10, checkbox_width=50, hover_color='grey50', border_color='black', fg_color='black', border_width=3)
                        button.grid(row=math.floor(i/5), column=i%5, padx=5, pady=5, sticky='nsew')
                        self.parameter_selections[label] = button

                self.data_table = pd.concat([self.data_table] + [pd.DataFrame(data, index=[0])], join='outer')
                self.graph_table = self.data_table.tail(self.time_map[self.graphing_interval.get()]).sort_values('Time')
                self.update_graph()

            except Exception as err:
                message_box = tk.Toplevel(self)
                message_box.configure(background='grey50')
                message_box.title('Error Message')
                message_box.geometry(f'300x150+{(int(self.winfo_screenwidth()/2) - 150)}+{(int(self.winfo_screenheight()/2) - 75)}')
                textbox = ctk.CTkTextbox(message_box, corner_radius=5, text_color='black', bg_color='grey50', fg_color='grey50', wrap='word')
                textbox.insert("0.0", err)
                textbox.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

                message_box.protocol("WM_DELETE_WINDOW", self._quit)


    def update_graph(self):
        if not self.graph_table.empty:
            y_min = None
            y_max = None
            handles = []
            labels = []
            x_data = self.graph_table['Time'].values
            x_min = x_data[0]
            x_max = x_data[-1]

            for param, button in self.parameter_selections.items():
                line = self.lines[param]
                if button:

                    if button.get():
                        handles.append(line)
                        line.set_visible(True)
                        y_data = self.graph_table[param].values
                        line.set_data(x_data, y_data)
                        last_datapoint = round(y_data[-1],3)
                        label = f'{param}: \n{last_datapoint}'
                        line.set_label(label)
                        labels.append(label)

                        # This section sets the x and y limits for viewing the graph based on only visible/selected parameters
                        if y_min:
                            if min(y_data) < y_min:
                                y_min = min(y_data)
                        else:
                            y_min = min(y_data)

                        if y_max:
                            if max(y_data) > y_max:
                                y_max = max(y_data)
                        else: 
                            y_max = max(y_data)
                        
                        # used to add margin to the view so that two graphs which are on the edges to not overlap with the axis, not nessisary for max
                        scaling_factor = (y_max - y_min) / 25
                        y_min -= scaling_factor
                        y_max += scaling_factor

                    else:
                        line.set_visible(False)  

            if not y_max == None and not y_min == None:
                self.ax1.set_xlim(x_min - 1, x_max + 1)
                self.ax1.set_ylim((y_min), (y_max))

            self.ax1.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 0.5 + .035 * (len(labels))), labelcolor='linecolor') # puts the legend to the side, and ajusts the verticle based on number of lines

            self.canvas1.draw_idle()


    def get_filename(self):

        filename = tk.filedialog.asksaveasfilename(defaultextension='.csv', title='Save output data as: ', filetypes = [('CSV files', '*csv')])
        self.filename = Path(filename)
        if self.filename.exists():
            self.filename.unlink()      # deletes any previous file with this name, they are asked if they want to overwrite by the tkinter save as window

        self.text_filename.set(filename[-25:])
        self.is_valid_filename = True


    def complete_message(self):

        exit_box = tk.Toplevel(self)
        exit_box.rowconfigure(0, weight=1)
        exit_box.columnconfigure(0, weight=1)
        exit_box.configure(background='grey50')
        exit_box.title('Complete!')
        exit_box.geometry(f'300x150+{(int(self.winfo_screenwidth()/2))}+{(int(self.winfo_screenheight()/2))}')
        exit_text_box = ctk.CTkLabel(exit_box, corner_radius=5,text_color='black', font=self.font1, bg_color='grey50', text='Your test is complete!', anchor='center')
        exit_text_box.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        exit_box.protocol("WM_DELETE_WINDOW", self._quit) 


    def read_data(self, port: object, start_time: float) -> dict:

        line = port.readline()
        ascii_data = line.decode(encoding='UTF-8')
        a = ast.literal_eval(ascii_data)
        c = {}
        for item in a:
            if 'Pack(mA)' in item:          #corrects for the fact that pack actually reports in centiamps, not (mA)
                c[item.replace('(mA)', '(A)')] = [a[item] / 100]
                c[item.replace('Pack(mA)', 'Pack_Power(Wh - Calculated)')] = [a[item] * a[item[:-4] + '(mV)'] / 1_000_00]   #Pack_Power(Wh - Calculated)

            elif '(mA)' in item:
                c[item.replace('(mA)', '(A)')] = [a[item] / 1000]
            elif '(mV)' in item:
                c[item.replace('(mV)', '(V)')] = [a[item] / 1000]
            else:
                c[item] = [a[item]]
        
        c['Inverter Pwr(W - Calculated)'] = [a['InvOut(mA)'] * a['InvOut(mV)'] / 1_000_000]
        c['Time'] = round(time.time() - start_time, 1)
        return c
    

    def save(self, header=True, mode='a'):

        if self.data_table is not None:
            self.data_table.sort_values('Time').to_csv(self.filename, mode=mode, header=header)
            print('saving')
        self.data_table = None    


    def _quit(self):

        self.destroy()
        sys.exit()


################################################################################################################
        
if __name__ == '__main__':
    app = APP()
    app.mainloop()