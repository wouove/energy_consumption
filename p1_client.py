import serial
import re
import logging as log

# ser = serial.Serial()
# ser.baudrate = 115200
# ser.bytesize=serial.SEVENBITS
# ser.parity=serial.PARITY_EVEN
# ser.stopbits=serial.STOPBITS_ONE
# ser.xonxoff=0
# ser.rtscts=0
# ser.timeout=20
# ser.port="/dev/ttyUSB0"
#
# try:
#     ser.open()
# except:
#     sys.exit ("Error opening %s. Program stopped."  % ser.name)
#
# p1_counter =0
# stack=[]
#
# while p1_counter < 36: # change this value
#     p1_line=''
#     try:
#         p1_raw = ser.readline()
#     except:
#         sys.exit ("Serial port %s can’t be read. Program stopped." % ser.name )
#     p1_str=str(p1_raw)
#     p1_line=p1_str.strip()
#     stack.append(p1_line)
#     p1_counter = p1_counter +1
#
# regex = re.compile(r'24.2.1')
#
# selected_row = list(filter(regex.search, stack))
# gas_value=float(selected_row[0][28:37]) # change these indices
#
# try:
#     ser.close()
# except:
#     sys.exit ("Ohoh %s. Program stopped." % ser.name )

BAUDRATE = 115200
BYTESIZE = serial.SEVENBITS
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE
XONXOFF = 0
RTSCTS = 0
TIMEOUT = 20
PORT = "/dev/ttyUSB0"


class P1client:
    def __init__(self):
        self.serial_object = serial.Serial()
        self.init_serial_object()

    def init_serial_object(self):
        self.serial_object.baudrate = BAUDRATE
        self.serial_object.bytesize = BYTESIZE
        self.serial_object.parity = PARITY
        self.serial_object.stopbits = STOPBITS
        self.serial_object.xonxoff = XONXOFF
        self.serial_object.rtscts = RTSCTS
        self.serial_object.timeout = TIMEOUT
        self.serial_object.port = PORT

    def read_p1_connection(self):
        self.open_serial_connection()
        measurement_value = self.parse_signal()
        self.close_serial_connection()
        return measurement_value

    def open_serial_connection(self):
        try:
            self.serial_object.open()
        except Exception as e:
            log.error(e)
            log.error(f"Error opening serial connection,  {self.serial_object.name}")

    def close_serial_connection(self):
        try:
            self.serial_object.close()
        except Exception as e:
            log.error(e)
            log.error(f"Error closing serial connection,  {self.serial_object.name}")

    def parse_signal(self):
        p1_counter = 0
        stack = []
        while p1_counter < 36:  # change this value
            # p1_line = ''
            try:
                p1_raw = self.serial_object.readline()
            except Exception as e:
                log.error(e)
                log.error(f"Serial port {self.serial_object.name} can’t be read. Program stopped.")
            p1_str = str(p1_raw)
            p1_line = p1_str.strip()
            stack.append(p1_line)
            p1_counter = p1_counter + 1

        regex = re.compile(r'24.2.1')

        selected_row = list(filter(regex.search, stack))
        measurement_value = float(selected_row[0][28:37])  # change these indices
        return measurement_value
