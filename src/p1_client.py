import serial
import re
import logging as log
import pandas as pd

# code taken from https://itheo.nl/reading-out-your-energy-meter/

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
        raw_data = self.read_signal()
        measurement_df = self.parse_signal(raw_data)
        self.close_serial_connection()
        return measurement_df

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

    def read_signal(self):
        p1_counter = 0
        stack = []
        while p1_counter < 36:  # change this value
            try:
                p1_raw = self.serial_object.readline()
                p1_line = p1_raw.decode('ascii').strip()
                print(f"p1_line: {p1_line}")
                stack.append(p1_line)
                p1_counter = p1_counter + 1
            except Exception as e:
                log.error(e)
                log.error(f"Serial port {self.serial_object.name} can’t be read. Program stopped.")
        return stack

    @staticmethod
    def parse_signal(stack):
        measurement_dict = {}
        for ser_data in stack:
            if re.match(r'(?=1-0:1.7.0)', ser_data):  # 1-0:1.7.0 = Actual usage in kW
                kw = ser_data[10:-4]  # Knip het kW gedeelte eruit (0000.54)
                # vermengvuldig met 1000 voor conversie naar Watt (540.0) en rond het af
                watt = int(float(kw) * 1000)

            if re.match(r'(?=1-0:1.8.1)', ser_data):
                consumption_1 = ser_data[10:-5]
                measurement_dict['consumption_low'] = consumption_1
                print(consumption_1)

            if re.match(r'(?=1-0:1.8.2)', ser_data):
                consumption_2 = ser_data[10:-5]
                measurement_dict['consumption_high'] = consumption_2
                print(consumption_2)

            if re.match(r'(?=1-0:2.8.1)', ser_data):
                production_1 = ser_data[10:-5]
                measurement_dict['production_low'] = production_1
                print(production_1)

            if re.match(r'(?=1-0:2.8.2)', ser_data):
                production_2 = ser_data[10:-5]
                measurement_dict['production_high'] = production_2
                print(production_2)

            return pd.DataFrame(measurement_dict, index=[0])
