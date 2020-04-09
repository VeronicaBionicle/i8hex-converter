import hex_maker as hex
from tkinter import Label, Entry, Button, Radiobutton, Tk, StringVar, IntVar, LEFT, CENTER, E, W
from tkinter.ttk import Label, Entry, Button, Radiobutton

def import_from_file():
    result_str.set(hex.read_from_file(entry_input_file.get(), extension = extension_input.get(), print_result = False))
def input_from_entry():
    result_str.set(entry_input_text.get())
def input_address():
    global init_address
    try:
        init_address = int(entry_input_address.get(), base.get())
    except:
        init_address = 0
        
def convert_to_hex():
    input_address()
    global init_address
    result_str.set(hex.convert_to_hex(hex.str_to_int(result_str.get(), base.get()), initial_address = init_address))
def export_file():
    hex.write_to_file(result_str.get(), entry_output_file.get(),extension = extension_output.get())
def convert_from_hex():
    info, bytes = hex.convert_from_hex(result_str.get())
    if (bytes != -1):
        result_str.set('Data:\n'+str(hex.str_to_int(bytes, 16))+'\nDetails:\n'+info)
    else:
        result_str.set(info)

master=Tk() #window
master.title("Intel HEX (I8HEX) converter")
digit_entry_default_text = StringVar()
digit_entry_default_text.set('0')
addr_entry_default_text = StringVar()
addr_entry_default_text.set('0')
input_default_name = StringVar()
input_default_name.set('input')
output_default_name = StringVar()
output_default_name.set('output')
#0 line
Label(master, text='Convert numbers to I8HEX and I8HEX to numbers', anchor=CENTER).grid(row=0, columnspan=5)
#1 line, "1" column - import file
extension_input = StringVar()
extension_input.set('txt')
Label(master, text='File name:', width = 12, anchor = E).grid(row=1)
entry_input_file = Entry(master, textvariable=input_default_name,width=15)
entry_input_file.grid(row=1,column=1)
import_button = Button(master, text='Import', command=import_from_file)
import_button.grid(row=1,column=4)
exten_hex_button = Radiobutton(master, text='.hex', variable=extension_input, value='hex')
exten_txt_button = Radiobutton(master, text='.txt', variable=extension_input, value='txt')
exten_hex_button.grid(row=1, column=2)
exten_txt_button.grid(row=1, column=3)
#2 line, "1" column - input
Label(master, text='Enter text:', width = 12, anchor = E).grid(row=2)
entry_input_text = Entry(master, textvariable=digit_entry_default_text, width=40)
entry_input_text.grid(row=2,column=1, columnspan = 3)
enter_button = Button(master, text='Enter', command=input_from_entry)
enter_button.grid(row=2,column=4)
#3 line - initial address
init_address = 0
Label(master, text='Initial address:', width = 12, anchor = E).grid(row=3, column = 0)
entry_input_address = Entry(master, textvariable=addr_entry_default_text, width=5, justify=LEFT)
entry_input_address.grid(row=3,column=1)
enter_address_button = Button(master, text='Enter', command=input_address)
enter_address_button.grid(row=3, column=2)
#4 line, "1" column - base
base = IntVar()
base.set(10)
Label(master, text='Choose base:', width = 12, anchor = E).grid(row=4, column = 0)
base_hex_button = Radiobutton(master, text='HEX', variable=base, value=16)
base_dec_button = Radiobutton(master, text='DEC', variable=base, value=10)
base_hex_button.grid(row=4, column=1)
base_dec_button.grid(row=4, column=2)
#5 line - convert buttons 
convert_to_hex_button = Button(master, text='Convert to hex', command=convert_to_hex)
convert_to_hex_button.grid(row=5,column=0, columnspan=2)
convert_from_hex_button = Button(master, text='Convert from hex', command=convert_from_hex)
convert_from_hex_button.grid(row=5,column=2, columnspan=2)
#6 line - export
extension_output = StringVar()
extension_output.set('txt')
Label(master, text='File name:', width = 12, anchor = E).grid(row=6)
entry_output_file = Entry(master, textvariable=output_default_name, width=15, justify=LEFT)
entry_output_file.grid(row=6,column=1)
import_button = Button(master, text='Export', command=export_file)
import_button.grid(row=6,column=4)
out_exten_hex_button = Radiobutton(master, text='.hex', variable=extension_output, value='hex')
out_exten_txt_button = Radiobutton(master, text='.txt', variable=extension_output, value='txt')
out_exten_hex_button.grid(row=6, column=2)
out_exten_txt_button.grid(row=6, column=3)
#7 line, "1" column - result
result_str = StringVar()
result_str.set('0')
result_text_box = Label(master, anchor=W, justify = LEFT, textvariable=result_str) # width=150
result_text_box.grid(row=7, columnspan=5)
master.mainloop()