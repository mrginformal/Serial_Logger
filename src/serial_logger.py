import serial
import serial.tools.list_ports
import pandas as pd
from pathlib import Path
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import math
import ast
import time

def setup_gui(dict1):
    root = tk.Tk()
    root.geometry('300x500')

    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)

    frame = tk.Frame(root, borderwidth=20, relief='ridge', width=900, height=900)
    frame.grid(row=0, column=0, sticky='nsew')

    dict2 = {}
    count = 0

    rows = math.ceil(len(dict1)/2)

    for row_index in range(rows):
        tk.Grid.rowconfigure(frame, row_index, weight=1)
        for col_index in range(2):
            if count < len(dict1):
                tk.Grid.columnconfigure(frame, col_index, weight=1)
                dict_item = list(dict1.keys())[count]
                dict2[dict_item] = tk.Variable()
                c = ttk.Checkbutton(frame, text=dict_item, variable=dict2[dict_item])
                c.grid(row=row_index, column=col_index, sticky='nsew')
                count += 1

    lbl = tk.Label(frame, text='select which parameters to display')
    lbl.grid(row=0, column=0, columnspan=2, sticky='nsew')

    exit_button = tk.Button(frame, text='Continue', borderwidth=5, command=root.destroy)
    exit_button.grid(row=rows, column=1, sticky='nsew')

    root.mainloop()
    filename = get_filename()
    
    lst = [i for i in dict2 if dict2[i].get() == '1']
    return lst, filename

def read_data(port, start_time):
    line=port.readline()
    ascii_data = line.decode(encoding='UTF-8')
    a = ast.literal_eval(ascii_data)
    c = {item: [a[item]] for item in a}
    c['Time'] = round(time.time() - start_time, 1)
    return c

def run():

    while True:
        ports = serial.tools.list_ports.comports()
        selected_port = None
        auto_var = input('Auto_Detect? (y/n):  ')

        if auto_var.lower() == 'y':
            vid = 1027                          #vid for ftdi usb --> serial converter, change to what ever chip you are using
            for p in ports:
                if p.vid == vid:
                    selected_port = serial.Serial(port=p.device, baudrate=115200, timeout=10)

            if not selected_port:
                print('No valid port found, try again')
            else:
                break
        
        else:
            port_list = [p for p in ports]
            port_names = [str(p.device) + ' >> ' + str(p.manufacturer) for p in port_list]
            print(f'detected COM ports: {port_names}')

            p_selection = input('Please type the exact name of the COM port you wish to use(example: COM9): ')

            for p in ports:
                if p.device == p_selection:
                    selected_port = serial.Serial(port=p.device, baudrate=115200, timeout=10)
            
            if not selected_port:
                print(f'No port named: {p_selection}')
            else:
                break

    start_time = time.time()
    table = None
    n = 0

    try:
        while True:
            try:
                pretty_data = read_data(selected_port, start_time)

                table = pd.concat([table] + [pd.DataFrame(pretty_data, index=[0])], join='outer')
                if n == 0:
                    selected_port.close()
                    selected_cols, filename = setup_gui(pretty_data)
                    selected_port.open()
                    print('starting')
                if not n % 5 and n != 0:
                    print(tabulate(table[selected_cols].tail(), headers=selected_cols))

                if not n % 300:
                    table.to_csv(filename, mode='w', index=False, header=True)
                n += 1
            except (ValueError, SyntaxError, NameError):
                print('Decode or Syntax Error detected, skipping datapoint')

    except KeyboardInterrupt:
        table.to_csv(filename, mode='w', index=False, header=True)
        return

def get_filename():
    filename = filedialog.asksaveasfilename(defaultextension='.csv', title='Save output data as: ', filetypes = [('CSV files', '*csv')])
    filename = Path(filename)

    if filename.exists():
        filename.unlink()      # deletes any previous file with this name, they are asked if they want to overwrite by the tkinter save as window

    return filename

def main():
    run()

if __name__ == '__main__':
    main()
