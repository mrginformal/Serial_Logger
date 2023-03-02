import serial
import serial.tools.list_ports
import pandas as pd
from pathlib import Path
from tabulate import tabulate
import tkinter as tk
from tkinter import ttk
import math
import datetime


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

    lst = [i for i in dict2 if dict2[i].get() == '1']
    return lst

def read_data(port):
    line=port.readline()
    ascii_data = line.decode(encoding='UTF-8')
    a = eval(ascii_data)
    c = {item: [a[item]] for item in a}
    c['DateTime'] = datetime.datetime.now()
    return c

def run(filename):

    ports = serial.tools.list_ports.comports()
    port_list = [p for p in ports]
    vid = 1027                          #vid for ftdi usb --> serial converter

    for p in ports:
        if p.vid == vid:
            selected_port = serial.Serial(port=p.device, baudrate=115200, timeout=10)


    table = None
    n = 0
    try:
        while True:
            pretty_data = read_data(selected_port)

            table = pd.concat([table] + [pd.DataFrame(pretty_data, index=[0])])
            if n == 0:
                table.to_csv(filename, index=False)
                selected_port.close()
                selected_cols = setup_gui(pretty_data)
                selected_port.open()
                print('starting')
            if not n % 5 and n != 0:
                print(tabulate(table[selected_cols].tail(), headers=selected_cols))

            if not n % 300:
                table.to_csv(filename, mode='a', index=False, header=False)
                table = None
            n += 1


    except KeyboardInterrupt:
        table.to_csv(filename, mode='a', index=False, header=False)
        return

def main():

    while True:
        try:
            filename = Path('Output_Files/' + input('Enter Filename to save as: ') + '.csv')
            break
        except:
            print('try again')
            pass
    
    run(filename)

main()
