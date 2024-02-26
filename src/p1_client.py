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
        measurement_df, measurement_dict = self.parse_signal(raw_data)
        self.close_serial_connection()
        return measurement_df, measurement_dict

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
        print(f'stack_data: {stack}')
        measurement_dict = {}
        for ser_data in stack:
            print(f'ser_data: {ser_data}')

            if re.match(r'(?=1-0:1.8.1)', ser_data):
                electricity_consumption_1 = ser_data[10:-5]
                measurement_dict['electricity_consumption_low'] = float(electricity_consumption_1)
                print(f'electricity_consumption_1: {electricity_consumption_1}')

            if re.match(r'(?=1-0:1.8.2)', ser_data):
                electricity_consumption_2 = ser_data[10:-5]
                measurement_dict['electricity_consumption_high'] = float(electricity_consumption_2)
                print(f'electricity_consumption_2: {electricity_consumption_2}')

            if re.match(r'(?=1-0:2.8.1)', ser_data):
                electricity_production_1 = ser_data[10:-5]
                measurement_dict['electricity_production_low'] = float(electricity_production_1)
                print(f'electricity_production_1: {electricity_production_1}')

            if re.match(r'(?=1-0:2.8.2)', ser_data):
                electricity_production_2 = ser_data[10:-5]
                measurement_dict['electricity_production_high'] = float(electricity_production_2)
                print(f'electricity_production_2: {electricity_production_2}')

            if re.match(r'(?=0-1:24.2.1)', ser_data):
                gas_consumption = ser_data[26:-4]
                measurement_dict['gas_consumption'] = float(gas_consumption)
                print(f'gas_consumption: {gas_consumption}')

            if re.match(r'(?=1-0:1.7.0)', ser_data):  # 1-0:1.7.0 = Actual usage in kW
                kw = ser_data[10:-4]  # Knip het kW gedeelte eruit (0000.54)
                # vermengvuldig met 1000 voor conversie naar Watt (540.0) en rond het af
                watt = int(float(kw) * 1000)
                measurement_dict['current_electricity_consumption'] = watt

        print(measurement_dict)
        return pd.DataFrame(measurement_dict, index=[0]), measurement_dict
