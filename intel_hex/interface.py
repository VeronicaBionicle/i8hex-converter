import hex_maker as hex
from tkinter import Label, Entry, Button, Radiobutton, Tk, StringVar, IntVar, LEFT, CENTER, E, W, scrolledtext, WORD, END
from tkinter.ttk import Label, Entry, Button, Radiobutton

def clear_and_print():
    result_text_box.delete(1.0, END)
    result_text_box.insert(1.0, result_str+'\n')

def import_from_file():
    global result_str
    result_str = hex.read_from_file(entry_input_file.get(), extension = extension_input.get(), print_result = False)
    clear_and_print()

def input_address():
    global init_address
    try:
        init_address = int(entry_input_address.get(), base.get())
    except:
        init_address = 0

def input_bytes_in_line():
    global init_bytes_in_line
    try:
        init_bytes_in_line = int(entry_input_bytes_in_line.get(), base.get())
    except:
        init_bytes_in_line = 16

def convert_to_hex():
    input_address()
    input_bytes_in_line()
    global init_address
    global init_bytes_in_line
    global result_str
    result_str = hex.convert_to_hex(hex.str_to_int(result_text_box.get(1.0, END), base.get()), initial_address = init_address, bytes_in_line = init_bytes_in_line)
    clear_and_print()

def export_file():
    global result_str
    if "error" in result_str or "error".title() in result_str:
        result_str = "Errors in data, writing canceled"
        clear_and_print()
    else:
        hex.write_to_file(result_str, entry_output_file.get(), extension = extension_output.get())

def convert_from_hex():
    global result_str
    info, bytes = hex.convert_from_hex(result_str)
    if (bytes != -1):
        result_str = 'Data:\n'+str(hex.str_to_int(bytes, 16))+'\nDetails:\n'+info
    else:
        result_str = info
    clear_and_print()

def clear_text():
    result_text_box.delete(1.0, END)

window=Tk() #window
window.title("Intel HEX (I8HEX) converter")
digit_entry_default_text = StringVar()
digit_entry_default_text.set('0')
addr_entry_default_text = StringVar()
addr_entry_default_text.set('0')
bytes_entry_default_text = StringVar()
bytes_entry_default_text.set('16')
input_default_name = StringVar()
input_default_name.set('input')
output_default_name = StringVar()
output_default_name.set('output')
extension_input = StringVar()
extension_input.set('txt')
extension_output = StringVar()
extension_output.set('txt')
base = IntVar()
base.set(10)
init_address = 0
init_bytes_in_line = 16
result_str = "0"
#textbox
result_text_box = scrolledtext.ScrolledText(window, width=120, height=20, font=("Consolas", 10)) 
result_text_box.grid(row=1, columnspan=5)
#1 line - input and import file
Label(window, text='Enter data or\nimport file to convert', width=20, anchor=W, font=12).grid(row=0, column=0) 
Label(window, text='File name:', width=10, anchor=E, font=12).grid(row=0, column=1)
entry_input_file = Entry(window, textvariable=input_default_name, width=20)
entry_input_file.grid(row=0, column=2, sticky=W)
#choose extention
exten_hex_button = Radiobutton(window, text='.hex', variable=extension_input, value='hex', width=5)
exten_txt_button = Radiobutton(window, text='.txt', variable=extension_input, value='txt', width=5)
exten_hex_button.grid(row=0, column=3, sticky=E)
exten_txt_button.grid(row=0, column=3, sticky=W)
import_button = Button(window, text='Import', command=import_from_file, width=20)
import_button.grid(row=0, column=4, sticky=E)
#clear textbox button
clear_button = Button(window, text='Clear', command=clear_text, width=120)
clear_button.grid(row=2, column=0, columnspan=5, pady=10)
#base of data
Label(window, text='Choose\nbase:', width=10, anchor=W, font=12).grid(row=3, column=0, sticky=W)
base_hex_button = Radiobutton(window, text='HEX', variable=base, value=16, width=5)
base_dec_button = Radiobutton(window, text='DEC', variable=base, value=10, width=5)
base_hex_button.grid(row=3, column=0, sticky=E)
base_dec_button.grid(row=3, column=0)
#initial address
Label(window, text='Initial\naddress:', font=12, anchor=W, width=15).grid(row=3, column=2, sticky=W)
entry_input_address = Entry(window, textvariable=addr_entry_default_text, width=5, justify=LEFT)
entry_input_address.grid(row=3, column=2)
#bytes in line
Label(window, text='Bytes in line\n(1-255):', width=15, anchor=W, font=12).grid(row=3, column=3)
entry_input_bytes_in_line = Entry(window, textvariable=bytes_entry_default_text, width=5, justify=LEFT)
entry_input_bytes_in_line.grid(row=3,column=3, sticky=E)
#convert buttons 
convert_to_hex_button = Button(window, text='Convert to hex', command=convert_to_hex, width=30)
convert_to_hex_button.grid(row=4, column=0, columnspan=2, pady=10)
convert_from_hex_button = Button(window, text='Convert from hex', command=convert_from_hex, width=30)
convert_from_hex_button.grid(row=4,column=3, columnspan=3, pady=10)
#export
Label(window, text='Export text to file', width=20, anchor=W, font=12).grid(row=5, column=0) 
Label(window, text='File name:', width=10, anchor=E, font=12).grid(row=5, column=1)
entry_output_file = Entry(window, textvariable=output_default_name, width=20, justify=LEFT)
entry_output_file.grid(row=5,column=2,sticky=W)
out_exten_hex_button = Radiobutton(window, text='.hex', variable=extension_output, value='hex', width=5)
out_exten_txt_button = Radiobutton(window, text='.txt', variable=extension_output, value='txt', width=5)
out_exten_hex_button.grid(row=5, column=3,sticky=E)
out_exten_txt_button.grid(row=5, column=3,sticky=W)
export_button = Button(window, text='Export', command=export_file)
export_button.grid(row=5,column=4,sticky=E, pady=10)
window.mainloop()