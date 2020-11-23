#Intel HEX (I8HEX) converter
import os
INPUT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "input")
OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "output")
for d in [INPUT_DIR, OUTPUT_DIR]:
    if not os.path.exists(d):
        os.mkdir(d)

'''
    Converts the list of int numbers to 8-bit Intel HEX (I8HEX) and prints it
    For example:
        :            01         0001        00         1a       e4
    Start code   Byte count   Address   Record type   Data   Checksum
    :00000001FF is end of file
    More info: https://en.wikipedia.org/wiki/Intel_HEX
'''
low = lambda number: (number & 0xFF)
high = lambda number: (number >> 8)

def hex_format(number, width_of_field, fill_symbol = '0'):
    hex_formatter = "{0:{fill}{width}x}"
    return hex_formatter.format(number, fill=fill_symbol, width=width_of_field)

def convert_to_hex(data, initial_address = 0, record_type = 0, bytes_in_line = 16):
    if  1 > bytes_in_line > 255:
        bytes_in_line = 1
    try:
        #make lines
        output_str = ""
        for address in range(0, len(data), bytes_in_line):
            data_bytes = data[address : address + bytes_in_line]
            data_bytes_str = ''.join([hex_format(byte, 2) for byte in data_bytes])
            checksum = len(data_bytes) + address + initial_address + sum(data_bytes) 
            checksum = low(0x100 - checksum)
            line = ":" + hex_format(len(data_bytes), 2) + hex_format(address + initial_address, 4) + hex_format(record_type, 2) + data_bytes_str + hex_format(checksum, 2)
            output_str += line.upper() + '\n'
        #end of file
        output_str += ":00000001FF"
        return output_str    
    except:
        return "Converting to hex error"

def convert_from_hex(data): 
    #convert str i8hex to formatted str
    try:
        line_data_format = "line: {:>3} bytes: {:>2} addr: {} rec.type: {} bytes: {} chksum: {} \n"
        line_EOF_format = "line: {:>3} {}"
        data_bytes = ""
        data_lines = data.split('\n')
        data_info = "Got lines: " + str(len(data_lines)) + '\n'
        for number, line in enumerate(data_lines):
            bytes_in_line = int(line[1:3],16)
            address = line[3:7]
            bytes = line[9:9+bytes_in_line*2]
            bytes = ' '.join([bytes[i:i+2] for i in range(0, len(bytes), 2)])
            checksum = line[9+bytes_in_line*2:11+bytes_in_line*2]
            if (line[7:9] == "00") :
                record_type = 'Data(00)'
                data_info += line_data_format.format(number+1, bytes_in_line, address, record_type, bytes, checksum)
                data_bytes += bytes.replace(' ', ',') + ','
            elif (line[7:9] == "01"):
                record_type = ('End of file(01)')
                data_info += line_EOF_format.format(number+1, record_type)
        return data_info, data_bytes
    except:
        return "Converting from hex error", -1

def read_from_file(file_name, extension = 'txt', print_result = False):
    try: 
        with open(os.path.join(INPUT_DIR,file_name +'.'+ extension), 'r') as input_file:
            content = input_file.read()
            if (print_result): print("Read from file "+ file_name +'.'+ extension + ":\n"+ content)
            return content 
    except: 
        return ("Error reading file " + file_name +'.'+ extension)

def write_to_file(data, file_name, extension = 'hex', print_result = False):
    try: 
        with open(os.path.join(OUTPUT_DIR,file_name +'.'+ extension), 'w+') as output_file: 
            output_file.write(data)
            if (print_result): print("Wrote to file" + file_name +'.'+ extension, "data:\n" + data)
    except: 
        return ("Error writing to file " + file_name +'.'+ extension)

def str_to_int(input_string, base = 10, print_result = False):
    try:
    #prepare data
        if (base == 16):
            input_string.replace("0x", "")
        data = input_string.replace(' ','').split(',') 
        if data[-1] == '':
            data = data[:-1]
        data = [int(byte, base) for byte in data]
        if (print_result): print("Converted data with base", base, ":", data)
        return data
    except:
        return "Converting str to int error"

if __name__ == "__main__":
    #write from console
    data = str_to_int(input_string = input("Enter data (delimiter ','): "), base = int(input("Base:")), print_result = True)
    data_str = convert_to_hex(data= data, initial_address = int(input("Enter initial address: ")), bytes_in_line = int(input("Bytes in line: ")), record_type=0)
    print(data_str)
    print(str_to_int(convert_from_hex(data_str)[1], 16))
    #write_to_file(data_str, 'out', extension='hex')
    #from file
    #data, bytes = convert_from_hex( read_from_file('test_hex', extension='hex'))
    #if (bytes != -1):
    #    write_to_file(str(str_to_int(bytes, 16))+'\n'+data, 'output', extension='txt', print_result=True) 